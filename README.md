---
title: Jivah-AI
emoji: 👅
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
---

# Tongue Image Classification Based on Traditional Thai Medicine Utilizing Deep Learning

## Manuscript Title 
[Leveraging Transfer Learning for Tri-Dhat Classification of Tongue Images in Traditional Thai Medicine](https://ph01.tci-thaijo.org/index.php/ecticit/article/view/260498)

## Journal
ECTI Transactions on Computer and Information Technology (ECTI-CIT)

## Software
Python 3.6.13 and TensorFlow 2.3.0 with Keras 2.4.0

## Dataset
Dataset is available at DOI: [10.21227/jy12-2c41](https://dx.doi.org/10.21227/56cx-0f96) and [10.5281/zenodo.12525501](https://doi.org/10.5281/zenodo.12525501)

## Abstract
Traditional Thai medicine (TTM) is a popular and increasingly accepted treatment option. In TTM, tongue diagnosis is a highly efficient method for assessing overall health, yet its accuracy can vary significantly depending on the practitioner's expertise. In this work, we hypothesize that deep learning-based transfer learning (TL) methods can achieve high accuracy in the Tri-Dhat classification of tongue images, a system that aligns with TTM principles and categorizes the tongue into three types: Vata, Pitta, and Kapha. We propose an approach that uses raw pixel data and artificial intelligence (AI) to support TTM diagnoses. 

For our analysis, we used a unique dataset of genuine tongue images collected from our university's TTM hospital. To prepare the data, we performed class balancing and data augmentation. We then developed TL techniques with a variety of pretrained deep learning models. Our experiments showed that the DenseNet121 and Xception models produced the most significant results with cropped image datasets, including both DSLR- and mobile-taken images. Notably, an ensemble of these models yielded the highest average predictions, achieving an accuracy of 0.96. We suggest that our methods could be effectively deployed in real-world scenarios to aid TTM practitioners in their diagnoses.

## Citation

Please also cite the following published papers:

* Damkliang, K., Sudkhaw, T., Yingtawee, T., Saearma, N., Moosigapong, K., Jaisamut, P., Chokpaisarn, J., Laman, S., Intan, A., & Ladam, A. (2025). [Leveraging Transfer Learning for Tri-Dhat Classification of Tongue Images in Traditional Thai Medicine](https://doi.org/10.37936/ecti-cit.2025193.260498). *ECTI Transactions on Computer and Information Technology (ECTI-CIT)*, 19(3), 442–457.
* Damkliang, K., Chumnaul, J., Sudkhaw, T., Yingtawee, T., & Saearm, N. (2025). [Multi-Model Approach for Tongue Image Classification in Traditional Thai Medicine](https://doi.org/10.3991/ijoe.v21i05.53671). *International Journal of Online and Biomedical Engineering (iJOE)*, 21(05), 47–62.

## Running the Web App

A production-style Streamlit web application is included to demonstrate the model's inference capabilities. The app allows users to upload an image of a tongue, predicts the corresponding dosha (Pitta, Vata, or Kapha), and provides tailored Ayurvedic dietary and lifestyle suggestions.

To run the application locally:
```bash
streamlit run app.py
