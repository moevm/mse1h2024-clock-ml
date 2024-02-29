package httpserver

import (
	"backend/internal/rabbitmq/publisher"

	"github.com/go-chi/chi/v5"
)

// Sets all server endpoints.
func SetRoutes(r *chi.Mux, p publisher.RabbitmqPublisher) {
	r.Route("/process", func(apiRoute chi.Router) {
		apiRoute.Post("/sendPicture", SendPicture(p))
	})
}
