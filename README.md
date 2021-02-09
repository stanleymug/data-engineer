# data-engineer
Data engineering on Google Cloud Platform - my continued learning journey

This repo is for various use cases for working with data on GCP that help me learn: 
1) Real-time data pipeline using Pub/Sub, Apache Beam/Dataflow and BigQuery. 
2) Batch data processing using Dataproc.
3) Machine learning with BigQuery and AutoML.

The goal is to iterate through the use cases and continuously look for other ways to work with data on GCP. The data sources will vary from sample Google data to generating fake data using Python to resemble common datasources. 


Streaming data pipeline on GCP
Using Pub/Sub, Apache Beam/Dataflow, and BigQuery

One of the key skills I wanted to develop as a data engineer was how to handle unbounded data (stream). This is a key skill, and as organisations aim to make better use of their data, one of the first things to think about is how to capture data – whether it’s from their web applications or devices (IoT). Given that I was limited to in terms of data I could use, I decided to create my own – but how? I had a particular idea of what data I wanted, so I thought about the most effective way to generate that data. I came across the Python Faker library – really useful for generating fake data based on any schema I want – Great! 

Architecture

![stream data1](https://user-images.githubusercontent.com/19821859/107396765-fa12cd00-6af5-11eb-862e-a777072d68f0.png) 


1.	Generate data randomly on Cloud Shell to a Pub/Sub topic.
2.	Connect Pub/Sub to Dataflow utilising Python and Apache Beam.
3.	Dataflow will do basic data cleansing and processing.
4.	BigQuery to receive data from Dataflow and store in a dataset with a single table. 
