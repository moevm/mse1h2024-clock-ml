package main

import (
	"backend/internal/config"
	"backend/internal/rabbitmq"
	"context"
	"log/slog"
	"os"
	"os/signal"
	"syscall"

	"backend/internal/httpserver"
	"backend/internal/logger"
	"backend/internal/restapi"
)

func main() {
	log := logger.New(slog.LevelDebug)

	cfg, err := config.New()
	if err != nil {
		log.Error("error while setting config: %v\n", err)
	}

	publisher, err := rabbitmq.New(cfg.Rabbit.URL)
	if err != nil {
		log.Error("error while creating publisher: %v\n", err)
	}
	defer publisher.Close()

	service := restapi.New(
		cfg.REST.Host,
		cfg.REST.Port,
	)

	server := httpserver.New(log, publisher, service, cfg.HTTP.Port)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	go func() {
		if err := server.Listen(ctx); err != nil {
			log.Error("server error: %v\n", err)
		}
	}()

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)

	sig := <-c
	log.Info("received %v signal\n", sig)
	cancel()

	<-ctx.Done()
}
