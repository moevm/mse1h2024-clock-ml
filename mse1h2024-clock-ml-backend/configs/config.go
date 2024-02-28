package configs

import (
	"io"
	"log"
	"os"

	"gopkg.in/yaml.v3"
)

type Config struct {
	App        `yaml:"app"`
	HTTP       `yaml:"http"`
	RabbitMQ   `yaml:"rabbitmq"`
}

type App struct {
	Name    string `yaml:"name" default:"mse1h2024-clock-ml-backend"`
	Version string `yaml:"version" default:"1.0.0"`
}

type HTTP struct {
	Port string `yaml:"port"`
}

type RabbitMQ struct {
	RabbitUrl string `yaml:"url"`
}

func NewConfig() (*Config, error) {
	file, err := os.Open(os.Getenv("CFG_PATH"))
	if err != nil {
		log.Fatalf("Error opening YAML file: %v", err)
		return nil, err
	}
	defer file.Close()

	data, err := io.ReadAll(file)
	if err != nil {
		log.Fatalf("Error reading YAML file: %v", err)
		return nil, err
	}

	var cfg Config
	err = yaml.Unmarshal(data, &cfg)
	if err != nil {
		log.Fatalf("Error unmarshalling YAML: %v", err)
		return nil, err
	}

	return &cfg, nil
}
