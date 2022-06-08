/* SPDX-License-Identifier: BSD 2-Clause "Simplified" License
 *
 * Created by:	Aakash Sen Sharma, May 2022
 * Copyright:	(C) 2022, Aakash Sen Sharma & Contributors
 */

package utils

import (
	"context"
	"os"
	"strings"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"go.uber.org/zap"
)
var db_conn *mongo.Client = nil

// Singleton pattern for accessing the database connection.
func GetConectionClient(db_uri string, ctx context.Context) (*mongo.Client, error) {
	if db_conn == nil {
		client, err := mongo.Connect(ctx, options.Client().ApplyURI(db_uri))
		if err != nil {
			return nil, err
		}
		db_conn = client
		return client, nil
	}
	return db_conn, nil
}

func SetupDevConfig(ctx context.Context, db *mongo.Database) {
		// Setup zap logger.
		var logger, _ = zap.NewDevelopment()
		defer logger.Sync()

		var result bson.D
		config_col := db.Collection("config")
		config_col.FindOne(ctx, bson.D{}).Decode(&result)

		if len(result) == 0 {
			config_col.Drop(ctx)
			config_col.InsertOne(ctx, bson.D{
				{"prefix", "2001:db8::/42"},
				{"plans", bson.D{
					{"v1-xsmall", bson.D{
						{"vcpus", 1},
						{"memory", 1},
						{"ssd", 4},
					}},
					{"v1-small", bson.D{
						{"vcpus", 2},
						{"memory", 4},
						{"ssd", 8},
					}},
					{"v1-medium", bson.D{
						{"vcpus", 4},
						{"memory", 8},
						{"ssd", 16},
					}},
					{"v1-large", bson.D{
						{"vcpus", 8},
						{"memory", 16},
						{"ssd", 32},
					}},
					{"v1-xlarge", bson.D{
						{"vcpus", 16},
						{"memory", 32},
						{"ssd", 64},
					}},
				}},
				{"oses", bson.D{
					{"debian", bson.D{
						{"version", 10.8},
						{"class", "debian"},
						{"url", "http://mirrors.fossho.st/fosshost/images/aarch64/current/debian-11.2.qcow2"},
						{"image", "debian.svg"},
					}},
					{"ubuntu", bson.D{
						{"version", 20.10},
						{"class", "ubuntu"},
						{"url", "http://mirrors.fossho.st/fosshost/images/aarch64/current/ubuntu.qcow2"},
						{"image", "ubuntu.svg"},
					}},
				}},
				{"key", "ssh-key"},
				{"port", 22},
				{"asn", 65530},
				{"email", bson.D{
					{"address", "user@example.com"},
					{"password", "1234567890"},
					{"server", "mail.example.com"},
				}},
				{"webhook", "https://example.com"},
				{"disabled_hosts", bson.A{}},
			})

			logger.Info("New DB setup complete!")
		} else {
			logger.Info("Configuration exists in database, cancelling configuration creation.")
		}
}

// If environment variable key is set then it returns the env var,
// else the fallback string.
func GetURI(env_key string, fallback string) string {
	if os.Getenv(env_key) == "" {
		return fallback
	} else {
		return strings.TrimSpace(os.Getenv(env_key))
	}
}
