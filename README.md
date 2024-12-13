# GCP Metric Automation

#### Set up Env

```
ENTERPRISE_NAME=<Enterprise Name>
GHC_TOKEN=<GHC Access TOKEN >
UPLOAD_LOCATION=<If excel needed to be in any particular location>
```

#### Download the Metrics Json

```bash
python download-copilot-metrics.py --token "$GHC_TOKEN" --enterprise "$ENTERPRISE_NAME"
```

#### Generate the report

```bash
python generate-copilot-report.py --enterprise "$ENTERPRISE_NAME" --uploadlocation "$UPLOAD_LOCATION"

```
