package robolytics

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"

	"github.com/beaglabs/chaveta-sdks/go/gen"
	"google.golang.org/protobuf/encoding/protojson"
	"google.golang.org/protobuf/proto"
)

// Client is a Robolytics client.
type Client struct {
	BaseURL      string
	clientID     string
	clientSecret string
	accessToken  string
	http         *http.Client
}

// ClientOption is a functional option for configuring the Client.
type ClientOption func(*Client)

// WithBaseURL sets the Chaveta API base URL.
func WithBaseURL(u string) ClientOption {
	return func(c *Client) { c.BaseURL = strings.TrimRight(u, "/") }
}

// WithClientCredentials sets OAuth2 M2M credentials.
func WithClientCredentials(clientID, clientSecret string) ClientOption {
	return func(c *Client) { c.clientID = clientID; c.clientSecret = clientSecret }
}

// NewClient creates a new Robolytics client.
func NewClient(opts ...ClientOption) *Client {
	c := &Client{
		BaseURL: "https://chaveta.beaglabs.com",
		http:    &http.Client{Timeout: 30 * time.Second},
	}
	for _, o := range opts {
		o(c)
	}
	return c
}

func (c *Client) token() (string, error) {
	if c.accessToken != "" {
		return c.accessToken, nil
	}
	if c.clientID == "" || c.clientSecret == "" {
		return "", fmt.Errorf("no credentials provided; use WithClientCredentials")
	}
	data := url.Values{
		"grant_type":    {"client_credentials"},
		"client_id":     {c.clientID},
		"client_secret": {c.clientSecret},
	}
	resp, err := c.http.PostForm(c.BaseURL+"/api/auth/oauth2/token", data)
	if err != nil {
		return "", fmt.Errorf("failed to obtain access token: %w", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("token endpoint returned %d", resp.StatusCode)
	}
	var tokenResp struct {
		AccessToken string `json:"access_token"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&tokenResp); err != nil {
		return "", err
	}
	c.accessToken = tokenResp.AccessToken
	return c.accessToken, nil
}

// SendEvent serializes and sends a RobotOpsEvent to the Chaveta ingest endpoint.
func (c *Client) SendEvent(event *gen.RobotOpsEvent) error {
	tok, err := c.token()
	if err != nil {
		return err
	}

	body, err := proto.Marshal(event)
	if err != nil {
		return fmt.Errorf("marshal: %w", err)
	}

	req, err := http.NewRequest("POST", c.BaseURL+"/api/v1/ingest", bytes.NewReader(body))
	if err != nil {
		return err
	}
	req.Header.Set("Authorization", "Bearer "+tok)
	req.Header.Set("Content-Type", "application/protobuf")

	resp, err := c.http.Do(req)
	if err != nil {
		return fmt.Errorf("ingest: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		var errResp struct {
			Error string `json:"error"`
		}
		io.ReadAll(resp.Body)
		_ = json.Unmarshal(nil, &errResp)
		if errResp.Error != "" {
			return fmt.Errorf("ingest failed (%d): %s", resp.StatusCode, errResp.Error)
		}
		return fmt.Errorf("ingest failed: %d", resp.StatusCode)
	}
	return nil
}

// SendEventJSON sends an event as JSON instead of protobuf.
func (c *Client) SendEventJSON(event *gen.RobotOpsEvent) error {
	tok, err := c.token()
	if err != nil {
		return err
	}

	body, err := protojson.Marshal(event)
	if err != nil {
		return fmt.Errorf("marshal json: %w", err)
	}

	req, err := http.NewRequest("POST", c.BaseURL+"/api/v1/ingest", bytes.NewReader(body))
	if err != nil {
		return err
	}
	req.Header.Set("Authorization", "Bearer "+tok)
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.http.Do(req)
	if err != nil {
		return fmt.Errorf("ingest: %w", err)
	}
	defer resp.Body.Close()
	return nil
}

func now() int64 {
	return time.Now().UnixNano()
}

// ScenarioStarted sends a ScenarioStarted event.
func (c *Client) ScenarioStarted(scenarioID, domain, softwareVersion string) error {
	return c.SendEvent(&gen.RobotOpsEvent{
		EventId:     proto.String(fmt.Sprintf("ev_%d", time.Now().UnixNano())),
		TimestampNs: proto.Int64(now()),
		Source:      proto.String("go-sdk"),
		Event: &gen.RobotOpsEvent_ScenarioStarted_{ScenarioStarted: &gen.ScenarioStarted{
			ScenarioId:      proto.String(scenarioID),
			Domain:          proto.String(domain),
			SoftwareVersion: proto.String(softwareVersion),
		}},
	})
}

// MissionCompleted sends a MissionCompleted event with arbitrary metrics.
func (c *Client) MissionCompleted(scenarioID string, status gen.MissionStatus, metrics map[string]float64) error {
	return c.SendEvent(&gen.RobotOpsEvent{
		EventId:     proto.String(fmt.Sprintf("ev_%d", time.Now().UnixNano())),
		TimestampNs: proto.Int64(now()),
		Source:      proto.String("go-sdk"),
		Event: &gen.RobotOpsEvent_MissionCompleted_{MissionCompleted: &gen.MissionCompleted{
			ScenarioId: proto.String(scenarioID),
			Status:     &status,
			Metrics:    metrics,
		}},
	})
}

// ObstacleEncountered sends an ObstacleEncountered event.
func (c *Client) ObstacleEncountered(scenarioID, obstacleClass string, collision bool, relativeSpeed float64) error {
	return c.SendEvent(&gen.RobotOpsEvent{
		EventId:     proto.String(fmt.Sprintf("ev_%d", time.Now().UnixNano())),
		TimestampNs: proto.Int64(now()),
		Source:      proto.String("go-sdk"),
		Event: &gen.RobotOpsEvent_ObstacleEncountered_{ObstacleEncountered: &gen.ObstacleEncountered{
			ScenarioId:    proto.String(scenarioID),
			ObstacleClass: proto.String(obstacleClass),
			Collision:     proto.Bool(collision),
			RelativeSpeed: proto.Float64(relativeSpeed),
		}},
	})
}

// ObjectIdentified sends an ObjectIdentified event.
func (c *Client) ObjectIdentified(scenarioID, className string, confidence float64) error {
	return c.SendEvent(&gen.RobotOpsEvent{
		EventId:     proto.String(fmt.Sprintf("ev_%d", time.Now().UnixNano())),
		TimestampNs: proto.Int64(now()),
		Source:      proto.String("go-sdk"),
		Event: &gen.RobotOpsEvent_ObjectIdentified_{ObjectIdentified: &gen.ObjectIdentified{
			ScenarioId: proto.String(scenarioID),
			ClassName:  proto.String(className),
			Confidence: proto.Float64(confidence),
		}},
	})
}
