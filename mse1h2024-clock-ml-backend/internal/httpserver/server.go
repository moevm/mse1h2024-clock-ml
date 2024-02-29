package httpserver

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"time"

	"backend/configs"
	"backend/internal/rabbitmq/publisher"
	"backend/internal/restapi"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

type Server struct {
	*http.Server
}

// Starts the server, waits for its graceful shutdown or context cancellation.
func (s *Server) Listen(ctx context.Context) error {
	errorChan := make(chan error)

	defer func() {
		close(errorChan)
	}()

	go func() {
		errorChan <- s.ListenAndServe()
	}()

	select {
	case <-ctx.Done():
		shutdownCtx, cancel := context.WithTimeout(
			context.Background(),
			5*time.Second,
		)
		defer cancel()

		if err := s.Shutdown(shutdownCtx); err != nil {
			fmt.Printf("Error during server shutdown: %v\n", err)
		}

		return ctx.Err()
	case err := <-errorChan:
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			return err
		}
		return nil
	}
}

// Creates a new Server instance.
func NewServer(
	p publisher.RabbitmqPublisher,
	service restapi.RestapiService,
) *Server {
	r := chi.NewRouter()

	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	cfg, _ := configs.NewConfig()

	s := &Server{
		Server: &http.Server{
			Addr:    fmt.Sprintf(":%d", cfg.HttpParams.Port),
			Handler: r,
		},
	}

	SetRoutes(r, p, service)

	return s
}
