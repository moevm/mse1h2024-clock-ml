package main

import (
	"context"
	"fmt"
	"log"

	"backend/configs"
	"backend/internal/httpserver"
	"backend/internal/rabbitmq/publisher"
)

func main() {
	cfg, err := configs.NewConfig()
	if err != nil {
		log.Fatalf("error while setting config: %v\n", err)
	}

	p, err := publisher.NewRabbitmqPublisher(cfg.RabbitUrl)
	if err != nil {
		log.Fatalf("error while creating publisher: %v\n", err)
	}

	server := httpserver.NewServer(fmt.Sprintf(":%s", cfg.Port), p)

	ctx := context.Background()
	if err := server.Listen(ctx); err != nil {
		log.Fatalf("server error: %v\n", err)
	}
}
