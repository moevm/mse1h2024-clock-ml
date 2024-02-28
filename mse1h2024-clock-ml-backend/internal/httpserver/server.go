package httpserver

import (
	"context"
	"errors"
	"net/http"
	"time"

	"backend/internal/rabbitmq/publisher"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

type Server struct {
	*http.Server
}

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
		return ctx.Err()
	case err := <-errorChan:
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			return err
		}
		return nil
	}
}

func NewServer(addr string, p publisher.RabbitmqPublisher) *Server {
	r := chi.NewRouter()

	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	s := &Server{
		Server: &http.Server{
			Addr:         addr,
			Handler:      r,
			ReadTimeout:  5 * time.Second,
			WriteTimeout: 10 * time.Second,
			IdleTimeout:  20 * time.Second,
		},
	}

	if s.ReadTimeout+s.WriteTimeout > s.IdleTimeout {
		panic("IdleTimeout must be set greater than the sum of ReadTimeout and WriteTimeout")
	}

	SetRoutes(r, p)

	return s
}
