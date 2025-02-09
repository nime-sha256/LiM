# Less is More (LiM) - Simplifying Network Traffic Classification

<p align="center">
   <a href="https://doi.org/10.5281/zenodo.14840527" target='_blank'><img src="https://zenodo.org/badge/924667348.svg" alt="DOI"></a>
   <a href=''><img src='https://img.shields.io/badge/license-MIT-000000.svg'></a> 
</p>

This repository contains the implementation of **LiM (Less is More)**, a lightweight network traffic classification approach using **NetMatrix** representation and an **XGBoost classifier**. LiM is based on the research paper:

> **"Less is More: Simplifying Network Traffic Classification Leveraging RFCs"**\
> *Nimesha Wickramasinghe, Arash Shaghaghi, Elena Ferrari, Sanjay Jha*\
> *Published at WWW Companion '25*\
> [Read it on ACM DL](https://doi.org/10.1145/3701716.3715492) | [Read it on ArXiv](https://arxiv.org/abs/2502.00586)

## 📌 Overview

Encrypted traffic classification is essential for **network security, monitoring, and management**. However, deep-learning-based methods often introduce unnecessary complexity, making them resource-intensive. **LiM** provides a **lightweight, RFC-compliant tabular representation** (NetMatrix) and achieves **high classification accuracy** with significantly **lower computational cost** than deep-learning models like **ET-BERT** and **YaTC**.

## 📂 Repository Structure

```
📁 LiM-Network-Traffic-Classification
│── requirements.txt             # Required dependencies
│── cstnet-tls1.3_5_packets.csv  # Pre-processed NetMatrix representation of the CSTNET-TLS1.3 dataset (10 classes)
│── pcap_to_netmatrix.py         # Script to convert custom PCAP files to NetMatrix representation
│── xgboost_classifier.py        # XGBoost classifier for network traffic classification
│── README.md                    # Project documentation
```

## 📥 Installation

Install the required dependencies using:

```sh
pip install -r requirements.txt
```

## 🔄 Converting Your Own Dataset

To use a **custom dataset**, follow these steps:

1. Replace your **PCAP file** directory in the `pcap_to_netmatrix.py` file.

2. Run the `pcap_to_netmatrix.py` script with the dataset path:

   ```sh
   python pcap_to_netmatrix.py
   ```

3. The script will process the packets and generate a **NetMatrix representation** as a CSV file.

## 🚀 Running the XGBoost Classifier

To perform network traffic classification using the pre-processed **NetMatrix representation**, execute:

```sh
python xgboost_classifier.py
```

### 🎯 Expected Output

The script will train and evaluate the **XGBoost model** and display metrics such as **accuracy, precision, recall, and F1-score**.

## 📊 Results Summary

| Model          | Accuracy | Recall | Precision | F1 Score |
| -------------- | -------- | ------ | --------- | -------- |
| **LiM (Ours)** | 0.942    | 0.942  | 0.943     | 0.942    |


## 🔧 Future Enhancements

- Expand evaluation to **other datasets** beyond CSTNET-TLS1.3.
- Extend classification to **new network traffic protocols**.
- Improve feature selection and representation methods for better performance.

## 🤝 Contribution

Feel free to **fork**, **contribute**, and **open issues** for improvements! For major changes, please open an issue first to discuss your ideas.

## 📜 Citation

If you find this work useful, please consider citing our paper:

```bibtex
@inproceedings{wickramasinghe2025lim,
  author = {Nimesha Wickramasinghe, Arash Shaghaghi, Elena Ferrari, Sanjay Jha},
  title = {Less is More: Simplifying Network Traffic Classification Leveraging RFCs},
  booktitle = {Companion Proceedings of the ACM Web Conference 2025},
  year = {2025},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  doi = {10.1145/3701716.3715492},
  series = {WWW '25}
}
```

## 📜 License

This project is licensed under the **MIT License**.

---

For questions or suggestions, contact:

- **Nimesha Wickramasinghe** - [*n.wickramasinghe@unsw.edu.au*](mailto\:n.wickramasinghe@unsw.edu.au)
- **Arash Shaghaghi** - [*a.shaghaghi@unsw.edu.au*](mailto\:a.shaghaghi@unsw.edu.au)

Happy coding! 🚀
