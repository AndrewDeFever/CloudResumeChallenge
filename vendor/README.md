# Self-hosted map dependencies

These files are served with the resume frontend from S3/CloudFront. The map's **Esri basemap tiles remain Esri-hosted**; do not mirror, cache, or redistribute the basemap images as static site assets.

| Runtime dependency | Source used for vendoring | Notes |
| --- | --- | --- |
| Leaflet JS/CSS | [Weather-and-Power-App vendor/leaflet](https://github.com/AndrewDeFever/Weather-and-Power-App/tree/main/frontend/static/vendor/leaflet) | Leaflet 1.9.4 |
| Leaflet default icon assets | Same Weather-and-Power-App `leaflet-assets.js` | Embedded local data URLs; no image CDN requests |
| MarkerCluster JS/CSS | [rstudio/leaflet markercluster plugin](https://github.com/rstudio/leaflet/tree/main/inst/htmlwidgets/plugins/Leaflet.markercluster) | Source provenance documented; verify library version before future upgrade |
| Leaflet.heat JS | [smittix/intercept vendor copy](https://github.com/smittix/intercept/tree/main/static/vendor/leaflet-heat) | Embedded simpleheat + Leaflet heat layer |

The initial resume page referenced Leaflet 1.9.4, leaflet.markercluster 1.5.3 and leaflet.heat 0.2.0 on unpkg. This vendoring change preserved Leaflet 1.9.4 and sourced compatible copies of the plugins from existing open-source repositories rather than claiming byte-for-byte equivalence with those CDN versions.

License and attribution notices in source files must be kept when updating. The map's Esri attribution remains in `CloudResumeChallenge.html`.

Deployment: `.github/workflows/CloudResumeChallengeDeploy.yml` publishes `vendor/` to the same S3 bucket as the HTML and invalidates CloudFront paths.
