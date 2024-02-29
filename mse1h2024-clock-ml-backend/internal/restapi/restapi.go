package restapi

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
)

type RestapiService struct {
	Url string
}

// Send request with encoded picture to estimation
func (s *RestapiService) SendPictureRequest(
	messageBody []byte,
) error {
	resp, err := http.Post(s.Url, "application/json", bytes.NewBuffer(messageBody))
	if err != nil {
		return ErrInvalidRequest
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK { 
		if err := handleErrorResponce(resp.Body); err != nil {
			log.Printf("handle response error: %v", err)
		}
		return ErrInvalidResponse
	}

	return nil
}

func handleErrorResponce(body io.ReadCloser) error {
	respData, err := io.ReadAll(body)
	if err != nil {
		return err
	}

	var errorMap map[string]interface{}
	err = json.Unmarshal(respData, &errorMap)
	if err != nil {
		return err
	}

	if errMessage, ok := errorMap["error"].(string); ok {
		log.Printf("response error: %s", errMessage)
		return nil
	}

	return errors.New("error while unmarshaling JSON response")
}

// Creates a new RestapiService instance.
func NewRestapiService(host string, port int) RestapiService {
	url := fmt.Sprintf(
		"http://%s:%d/process/estimation",
		host,
		port,
	)

	return RestapiService{
		Url: url,
	}
}
