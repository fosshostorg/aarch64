/* SPDX-License-Identifier: BSD 2-Clause "Simplified" License
 *
 * Created by:	Aakash Sen Sharma, May 2022
 * Copyright:	(C) 2022, Aakash Sen Sharma & Contributors
 */
package main

import (
	"context"
	"fosshost/api/utils"
	"os"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/joho/godotenv"

	"go.uber.org/zap"
)

func main() {
	// Setup zap logger.
	logger, _ := zap.NewDevelopment()
	defer logger.Sync()

	// Load .env configuration.
	if err := godotenv.Load(); err != nil {
		logger.Error("Error loading .env file", zap.String("Error", err.Error()))
	}

	// Fetch URI's.
	mongodb_uri := utils.GetURI("AARCH64_DB_URI", "mongodb://localhost:27017")
	nsq_uri := utils.GetURI("AARCH64_NSQ_URI", "http://[fd0d:944c:1337:aa64:1::]:4151")
	logger.Info("URI:", zap.String("MongoDB", mongodb_uri), zap.String("NSQ", nsq_uri))

	// Create connection context with a timeout of 10 seconds.
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Establish a connection with the MongoDB instance.
	client, err := utils.GetConectionClient(mongodb_uri, ctx)
	if err != nil {
		logger.Error("Failed to establish MongoDB connection.", zap.String("Connect Error", err.Error()))
	}
	db := client.Database("aarch64")

	// Close the connection to MongoDB
	defer func() {
		if err = client.Disconnect(ctx); err != nil {
			logger.Error("Failed to disconnect from MongoDB instance", zap.String("Disconnect Error", err.Error()))
		}
	}()

	// Conditional config setup for dev environments.
	if os.Getenv("AARCH64_DEV_CONFIG_DATABASE") != "" {
		utils.SetupDevConfig(ctx, db)
	}

	// Creating the API instance.
	api := fiber.New(fiber.Config{
		Prefork:       false,
		CaseSensitive: false,
		StrictRouting: false,
		ServerHeader:  "fosshost-aarch64",
		AppName:       "Aarch64 API",
	})

	// Register routes.
	api.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, World 👋!")
	})

	// Start the api.
	api.Listen(":3000")
}
