#!/usr/bin/env bash

./curlbash.sh -D "create a new DOcker-based Laravel app"   -R "https://laravel.com/docs/11.x" markdown https://laravel.build/example-app
./curlbash.sh -D "install Docker"                          -R "https://docs.docker.com/engine/install/ubuntu/" markdown https://get.docker.com
./curlbash.sh -D "install FrankenPHP"                      -R "https://frankenphp.dev/docs/"  markdown https://frankenphp.dev/install.sh
./curlbash.sh -D "install PHP, Composer and Laravel"       -R "https://php.new/"              markdown https://php.new/install/mac/8.4
./curlbash.sh -D "install Sandstorm self-hosting platform" -R "https://sandstorm.org/install" markdown https://install.sandstorm.io
./curlbash.sh -D "install basher, bash package manager"    -R "https://www.basher.it/"        markdown https://raw.githubusercontent.com/basherpm/basher/master/install.sh
./curlbash.sh -D "install homebrew, MacOS package manager" -R "https://brew.sh/"              markdown https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
./curlbash.sh -D "install nvm Node Version Manager"        -R "https://github.com/nvm-sh/nvm" markdown https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh
./curlbash.sh -D "install Google Cloud SDK"                -R "https://cloud.google.com/sdk/docs/install-sdk" markdown https://sdk.cloud.google.com