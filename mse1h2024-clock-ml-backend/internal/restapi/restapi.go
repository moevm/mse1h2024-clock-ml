package restapi

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type Service struct {
	Url string
}

// SendPictureRequest sends request with encoded picture to estimation
func (s *Service) SendPictureRequest(
	messageBody []byte,
) error {
	resp, err := http.Post(s.Url, "application/json", bytes.NewBuffer(messageBody))
	if err != nil {
		return ErrInvalidRequest
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return handleErrorResponce(resp.Body)
	}

	return nil
}

func handleErrorResponce(body io.ReadCloser) error {
	respData, err := io.ReadAll(body)
	if err != nil {
		return err
	}

	var response Reponse
	err = json.Unmarshal(respData, &response)
	if err != nil {
		return err
	}

	if response.ErrorMessage != "" {
		return fmt.Errorf("response error: %s", response.ErrorMessage)
	}

	return nil
}

// New creates a new Service instance.
func New(host string, port int) Service {
	url := fmt.Sprintf(
		"http://%s:%d/process/estimation",
		host,
		port,
	)

	return Service{
		Url: url,
	}
}
