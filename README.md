# Kenya Sign Language to Text Captioning Using 3D Neural Networks

This project implements a video-to-text captioning system for **Kenya Sign Language (KSL)** using deep learning models, specifically 3D Convolutional Neural Networks (CNNs) and Recurrent Neural Networks (RNNs), aimed at bridging the communication gap between the Deaf and hearing communities in Kenya.

## 🔍 Overview

Kenya Sign Language (KSL) is a rich, expressive language used by the Deaf community in Kenya. However, limited understanding of KSL by the general public hinders effective communication. This project proposes an AI-based system that:
- Recognizes KSL signs from video input.
- Generates real-time text captions.
- Enhances inclusivity and accessibility.

## 🎯 Objectives

- Develop a 3D CNN + RNN model to classify KSL gestures.
- Preprocess video inputs for spatial-temporal modeling.
- Augment and segment data for improved performance.
- Deploy a user-facing web interface for video captioning.

## 🧠 Methodology

- **Data Processing**: Video-to-frame conversion, resizing, normalization, segmentation.
- **Model Architecture**: 3D CNNs for spatial feature extraction + GRU for temporal dynamics.
- **Training**: Implemented in TensorFlow with early stopping and validation split.
- **Deployment**: Flask-based backend; client interface allows video upload or recording.

## 🛠️ Technologies Used

- Python, TensorFlow, Flask, JavaScript
- Google Colab (GPU), Cloudinary for media storage
- HTML/CSS for frontend interaction
- CNN + GRU based deep learning architecture

## 📊 Results

- Achieved ~80% training accuracy, ~70% validation accuracy.
- System capable of real-time inference and robust to noisy inputs.
- Supports core signs: *Come*, *Home*, *I’m*, *Work*.

## 🌐 Demo Features

- Upload or record KSL video via web interface.
- Real-time inference and caption display.
- Backend processing and cloud-based video handling.

## 🚀 Future Enhancements

- Expand vocabulary and dataset.
- Integrate attention mechanisms.
- Implement feedback loop and personalization.
- Optimize for edge devices and mobile inference.

## 📄 License

MIT License

## 👤 Author

**Owino Philip Oyoo**  
BSc. Electronic & Computer Engineering  
[GitHub Profile](https://github.com/OYOOOWINO)

