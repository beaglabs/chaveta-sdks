use reqwest::header::{AUTHORIZATION, CONTENT_TYPE};
use serde_json::json;
use uuid::Uuid;

const DEFAULT_BASE_URL: &str = "https://chaveta.beaglabs.com";

/// Robolytics client for sending events to the Chaveta ingest API.
pub struct Client {
    base_url: String,
    client_id: Option<String>,
    client_secret: Option<String>,
    access_token: Option<String>,
    http: reqwest::Client,
}

impl Client {
    pub fn new(
        client_id: &str,
        client_secret: &str,
    ) -> Self {
        Self {
            base_url: DEFAULT_BASE_URL.to_string(),
            client_id: Some(client_id.to_string()),
            client_secret: Some(client_secret.to_string()),
            access_token: None,
            http: reqwest::Client::new(),
        }
    }

    pub fn with_base_url(mut self, url: &str) -> Self {
        self.base_url = url.trim_end_matches('/').to_string();
        self
    }

    async fn token(&mut self) -> Result<String, Box<dyn std::error::Error>> {
        if let Some(ref token) = self.access_token {
            return Ok(token.clone());
        }
        let (cid, csec) = match (&self.client_id, &self.client_secret) {
            (Some(id), Some(sec)) => (id.clone(), sec.clone()),
            _ => return Err("No credentials provided".into()),
        };
        let resp = self.http
            .post(format!("{}/api/auth/oauth2/token", self.base_url))
            .form(&[
                ("grant_type", "client_credentials"),
                ("client_id", &cid),
                ("client_secret", &csec),
            ])
            .send()
            .await?;
        let data: serde_json::Value = resp.json().await?;
        let token = data["access_token"].as_str()
            .ok_or("Missing access_token")?
            .to_string();
        self.access_token = Some(token.clone());
        Ok(token)
    }

    async fn send(&mut self, event: serde_json::Value) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
        let token = self.token().await?;
        let resp = self.http
            .post(format!("{}/api/v1/ingest", self.base_url))
            .header(AUTHORIZATION, format!("Bearer {}", token))
            .header(CONTENT_TYPE, "application/json")
            .json(&event)
            .send()
            .await?;
        if !resp.status().is_success() {
            return Err(format!("Ingest failed: {}", resp.status()).into());
        }
        Ok(resp.json().await?)
    }

    fn event_id() -> String { Uuid::new_v4().to_string() }
    fn ts() -> i64 {
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos() as i64
    }

    pub async fn scenario_started(
        &mut self,
        scenario_id: &str,
        domain: &str,
        software_version: &str,
    ) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
        self.send(json!({
            "eventId": Self::event_id(),
            "timestampNs": Self::ts(),
            "source": "rust-sdk",
            "sourceVersion": "1.0.0",
            "scenarioStarted": {
                "scenarioId": scenario_id,
                "domain": domain,
                "softwareVersion": software_version,
            }
        })).await
    }

    pub async fn mission_completed(
        &mut self,
        scenario_id: &str,
        status: i32,
        metrics: serde_json::Value,
    ) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
        self.send(json!({
            "eventId": Self::event_id(),
            "timestampNs": Self::ts(),
            "source": "rust-sdk",
            "sourceVersion": "1.0.0",
            "missionCompleted": {
                "scenarioId": scenario_id,
                "status": status,
                "metrics": metrics,
            }
        })).await
    }

    pub async fn obstacle_encountered(
        &mut self,
        scenario_id: &str,
        obstacle_class: &str,
        collision: bool,
        relative_speed: f64,
    ) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
        self.send(json!({
            "eventId": Self::event_id(),
            "timestampNs": Self::ts(),
            "source": "rust-sdk",
            "sourceVersion": "1.0.0",
            "obstacleEncountered": {
                "scenarioId": scenario_id,
                "obstacleClass": obstacle_class,
                "collision": collision,
                "relativeSpeed": relative_speed,
            }
        })).await
    }

    pub async fn object_identified(
        &mut self,
        scenario_id: &str,
        class_name: &str,
        confidence: f64,
    ) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
        self.send(json!({
            "eventId": Self::event_id(),
            "timestampNs": Self::ts(),
            "source": "rust-sdk",
            "sourceVersion": "1.0.0",
            "objectIdentified": {
                "scenarioId": scenario_id,
                "className": class_name,
                "confidence": confidence,
            }
        })).await
    }
}
