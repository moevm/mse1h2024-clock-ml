package main

import (
	"context"
	"log/slog"
	"os"
	"os/signal"
	"syscall"

	"backend/configs"
	"backend/internal/httpserver"
	"backend/internal/logger"
	"backend/internal/rabbitmq/publisher"
	"backend/internal/restapi"
)

func main() {
	log := logger.New(slog.LevelDebug)

	cfg, err := configs.New()
	if err != nil {
		log.Error("error while setting config: %v\n", err)
	}

	publisher, err := publisher.New(cfg.RabbitParams.RabbitUrl)
	if err != nil {
		log.Error("error while creating publisher: %v\n", err)
	}
	defer publisher.Close()

	service := restapi.New(
		cfg.EstimationParams.Host, 
		cfg.EstimationParams.Port,
	)

	server := httpserver.NewServer(log, publisher, service, cfg.HttpParams.Port)

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
