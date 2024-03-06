package httpserver

import (
	"backend/internal/rabbitmq/publisher"
	"backend/internal/restapi"

	"github.com/go-chi/chi/v5"
)

// SetRoutes sets all server endpoints
func SetRoutes(
	r *chi.Mux,
	p publisher.RabbitmqPublisher,
	s restapi.RestapiService,
) {
	r.Route("/process", func(apiRoute chi.Router) {
		apiRoute.Post("/sendPicture", SendPicture(p, s))
	})
}
