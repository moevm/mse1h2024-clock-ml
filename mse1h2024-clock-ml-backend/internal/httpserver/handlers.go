package httpserver

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"

	"backend/internal/rabbitmq/publisher"
	"backend/configs"
)

const (
	paramName = "broker"
	queueName = "estimation"
) 

// Processes requests for sending pictures using amqp or rest, based on 'broker' queryParam.
func SendPicture(
	p publisher.RabbitmqPublisher,
) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		queryParams := r.URL.Query()
		isBroker := queryParams.Get(paramName)
		
		isBrokerValue, err := strconv.ParseBool(isBroker)
		if err != nil {
			http.Error(
				w,
				"invalid broker boolean parameter",
				http.StatusBadRequest,
			)
			return
		}

		var imageRequest ImageRequest
		if err := decodeJSON(r, &imageRequest); err != nil {
			http.Error(w, "invalid JSON format", http.StatusBadRequest)
			return
		}

		messageBody, err := json.Marshal(imageRequest)
		if err != nil {
			http.Error(
				w,
				"Failed to marshal JSON",
				http.StatusInternalServerError,
			)
			return
		}
		
		if isBrokerValue {
			err = p.PublishMessage(queueName, messageBody)
			if err != nil {
				return
			}
		} else {
			sendRequestToEstimation(w, messageBody)
			return
		}

		w.WriteHeader(http.StatusOK)
	}
}

func sendRequestToEstimation(w http.ResponseWriter, payload []byte) {	
	cfg, _ := configs.NewConfig()
	url := fmt.Sprintf(
		"http://%s:%d/process/estimation", 
		cfg.EstimationParams.Host,
		cfg.EstimationParams.Port,
	)

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(payload))
	if err != nil {
		http.Error(
			w,
			"invalid estimation request",
			http.StatusBadRequest,
		)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		http.Error(
			w,
			fmt.Sprintf(
				"estimation service returned non-OK status: %d", 
				resp.StatusCode,
			),
			http.StatusBadGateway,
		)
		return
	}

	w.WriteHeader(http.StatusOK)
}

func decodeJSON(r *http.Request, v interface{}) error {
	return json.NewDecoder(r.Body).Decode(v)
}
