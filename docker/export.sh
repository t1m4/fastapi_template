#/bin/bash

export $(grep -v --regex='^#.*' .env | xargs)