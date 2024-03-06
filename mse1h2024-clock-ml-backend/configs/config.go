package configs

import (
	"io"
	"log"
	"os"

	"gopkg.in/yaml.v3"
)

var configPath = os.Getenv("CFG_PATH")

type Config struct {
	AppInfo          App        `yaml:"app"`
	HttpParams       HTTP       `yaml:"http"`
	RabbitParams     RabbitMQ   `yaml:"rabbitmq"`
	EstimationParams Estimation `yaml:"estimation"`
}

type App struct {
	Name    string `yaml:"name" default:"mse1h2024-clock-ml-backend"`
	Version string `yaml:"version" default:"1.0.0"`
}

type HTTP struct {
	Port int `yaml:"port"`
}

type RabbitMQ struct {
	RabbitUrl string `yaml:"url"`
}

type Estimation struct {
	Port int    `yaml:"port"`
	Host string `yaml:"host"`
}

// NewConfig creates a singleton instance of the Config struct.
func New() (*Config, error) {
	file, err := os.Open(configPath)
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
