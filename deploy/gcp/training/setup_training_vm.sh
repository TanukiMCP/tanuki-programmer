#!/bin/bash
# This script sets up a Google Compute Engine VM for model training.
# It creates a new VM with a T4 GPU and a pre-installed deep learning image.

# --- Configuration ---
export REGION="us-central1"
export ZONE="us-central1-a"
export INSTANCE_NAME="tanuki-training-vm"
export MACHINE_TYPE="n1-standard-8" # 8 vCPUs, 30 GB memory
export IMAGE_FAMILY="tf-latest-gpu" # TensorFlow Enterprise 2.x with CUDA 11.3
export IMAGE_PROJECT="deeplearning-platform-release"
export ACCELERATOR_TYPE="nvidia-tesla-t4"
export ACCELERATOR_COUNT="1"

# --- Create VM ---
echo "Creating GCE VM: $INSTANCE_NAME..."

gcloud compute instances create "$INSTANCE_NAME" \
    --zone="$ZONE" \
    --image-family="$IMAGE_FAMILY" \
    --image-project="$IMAGE_PROJECT" \
    --machine-type="$MACHINE_TYPE" \
    --accelerator="type=$ACCELERATOR_TYPE,count=$ACCELERATOR_COUNT" \
    --maintenance-policy="TERMINATE" \
    --restart-on-failure \
    --boot-disk-size=200GB \
    --metadata="install-nvidia-driver=True"

echo "VM '$INSTANCE_NAME' created."
echo "You can SSH into the VM using:"
echo "gcloud compute ssh --zone $ZONE $INSTANCE_NAME" 