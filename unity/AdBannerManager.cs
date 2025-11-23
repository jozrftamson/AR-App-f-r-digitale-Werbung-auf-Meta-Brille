using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;
using TMPro;

/// <summary>
/// Fetches nearby ads from a REST API and anchors simple banner prefabs on detected planes.
/// Designed for Meta Quest / Meta Smart Glasses prototypes that use AR Foundation + OpenXR.
/// </summary>
[RequireComponent(typeof(ARPlaneManager))]
[RequireComponent(typeof(ARAnchorManager))]
public class AdBannerManager : MonoBehaviour
{
    [Header("Managers")]
    [SerializeField] private ARPlaneManager planeManager;
    [SerializeField] private ARAnchorManager anchorManager;

    [Header("Prefabs & UI")]
    [Tooltip("World-space canvas prefab that contains a RawImage + TMP_Text for the ad visuals.")]
    [SerializeField] private GameObject bannerPrefab;

    [Header("Networking")]
    [SerializeField] private string adsApiEndpoint = "https://api.example.com/ads/nearby";
    [SerializeField] private float refreshIntervalSeconds = 15f;

    private readonly List<AdPayload> cachedAds = new();
    private bool isRequestRunning;

    private void Awake()
    {
        planeManager = planeManager ?? GetComponent<ARPlaneManager>();
        anchorManager = anchorManager ?? GetComponent<ARAnchorManager>();
        planeManager.planesChanged += HandlePlanesChanged;
    }

    private IEnumerator Start()
    {
        yield return StartCoroutine(RequestLocationPermission());
        StartCoroutine(FetchAdsLoop());
    }

    private IEnumerator FetchAdsLoop()
    {
        while (true)
        {
            if (!isRequestRunning)
            {
                yield return StartCoroutine(FetchAds());
            }
            yield return new WaitForSeconds(refreshIntervalSeconds);
        }
    }

    private IEnumerator FetchAds()
    {
        if (!Input.location.isEnabledByUser)
        {
            Debug.LogWarning("GPS disabled. Using fallback coordinates.");
        }

        var lat = Input.location.status == LocationServiceStatus.Running ? Input.location.lastData.latitude : 51.0504f;
        var lng = Input.location.status == LocationServiceStatus.Running ? Input.location.lastData.longitude : 13.7373f;
        var radius = 200;

        var url = string.Format("{0}?lat={1}&lng={2}&radius={3}", adsApiEndpoint, lat, lng, radius);
        using var request = UnityWebRequest.Get(url);
        isRequestRunning = true;
        yield return request.SendWebRequest();
        isRequestRunning = false;

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError("Ad fetch failed: " + request.error);
            yield break;
        }

        var json = JsonUtility.FromJson<AdList>("{" + "\"ads\":" + request.downloadHandler.text + "}");
        cachedAds.Clear();
        cachedAds.AddRange(json.ads);
    }

    private void HandlePlanesChanged(ARPlanesChangedEventArgs args)
    {
        if (cachedAds.Count == 0)
        {
            return;
        }

        foreach (var plane in args.added)
        {
            if (plane.alignment != PlaneAlignment.Vertical)
            {
                continue; // focus on facades/windows for this prototype
            }

            var payload = cachedAds[0];
            SpawnBanner(payload, plane);
            cachedAds.RemoveAt(0);

            if (cachedAds.Count == 0)
            {
                break;
            }
        }
    }

    private void SpawnBanner(AdPayload ad, ARPlane plane)
    {
        var pose = new Pose(plane.center, Quaternion.LookRotation(plane.normal));
        var anchor = anchorManager.AddAnchor(pose);
        if (anchor == null)
        {
            Debug.LogWarning("Failed to create anchor for ad " + ad.id);
            return;
        }

        var banner = Instantiate(bannerPrefab, anchor.transform);
        banner.AddComponent<BillboardToCamera>();
        banner.transform.localScale = Vector3.one * Mathf.Clamp(ad.preferredSizeMeters, 0.5f, 4f);

        var text = banner.GetComponentInChildren<TMP_Text>();
        if (text != null)
        {
            text.text = ad.title;
        }

        var image = banner.GetComponentInChildren<UnityEngine.UI.RawImage>();
        if (image != null && !string.IsNullOrEmpty(ad.media_url))
        {
            StartCoroutine(LoadTexture(ad.media_url, image));
        }
    }

    private IEnumerator LoadTexture(string url, UnityEngine.UI.RawImage target)
    {
        using var request = UnityWebRequestTexture.GetTexture(url);
        yield return request.SendWebRequest();
        if (request.result == UnityWebRequest.Result.Success)
        {
            target.texture = DownloadHandlerTexture.GetContent(request);
        }
        else
        {
            Debug.LogWarning("Failed to load ad texture: " + request.error);
        }
    }

    private IEnumerator RequestLocationPermission()
    {
        if (!Input.location.isEnabledByUser)
        {
            yield break;
        }

        Input.location.Start();
        var maxWait = 5f;
        while (Input.location.status == LocationServiceStatus.Initializing && maxWait > 0)
        {
            yield return new WaitForSeconds(1);
            maxWait -= 1f;
        }

        if (Input.location.status != LocationServiceStatus.Running)
        {
            Debug.LogWarning("GPS unavailable, continuing with static coordinates.");
        }
    }

    [System.Serializable]
    private class AdList
    {
        public List<AdPayload> ads = new();
    }

    [System.Serializable]
    private class AdPayload
    {
        public string id;
        public string title;
        public string media_url;
        public float preferredSizeMeters = 1.2f;
    }
}

/// <summary>
/// Simple billboard helper so the banner always faces the user.
/// </summary>
public class BillboardToCamera : MonoBehaviour
{
    private void LateUpdate()
    {
        var cam = Camera.main;
        if (cam == null)
        {
            return;
        }

        transform.LookAt(cam.transform);
        transform.Rotate(0f, 180f, 0f);
    }
}
