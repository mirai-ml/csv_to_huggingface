# CSV to Hugging Face

A Python library for converting CSV data to optimized formats and uploading to Hugging Face datasets. This package provides tools for data optimization, dataset card generation, and seamless integration with Hugging Face.

## Features

- Convert CSV files to optimized Parquet format
- Automatic data type optimization to minimize memory usage
- Generate comprehensive dataset cards for Hugging Face
- Upload datasets to Hugging Face with proper formatting
- Analyze dataset statistics and generate metadata
- Support for private and public datasets
- Streaming support for large datasets

## Installation

```bash
pip install csv_to_huggingface
```

For development installation:

```bash
git clone https://github.com/mirai-ml/csv_to_huggingface.git
cd csv_to_huggingface
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```python
from csv_to_huggingface import DataProcessor, DatasetCardGenerator, HuggingFaceManager

# Initialize components
processor = DataProcessor()
card_generator = DatasetCardGenerator(
    dataset_name="my_dataset",
    description="A sample dataset",
    task_categories=["text-classification"]
)
hf_manager = HuggingFaceManager(token="your_token")

# Convert CSV to Parquet
parquet_path = processor.convert_to_parquet("data.csv")

# Analyze data
stats = processor.analyze_data(pd.read_parquet(parquet_path))

# Generate dataset card
card_generator.add_data_stats(stats)
card_generator.save_card("dataset-card.json")

# Upload to Hugging Face
hf_manager.upload_dataset(
    dataset_path="path/to/dataset",
    dataset_name="my_dataset",
    private=False
)
```

### Advanced Usage

#### Data Type Optimization

```python
# Optimize data types manually
df = pd.read_csv("data.csv")
df_optimized = processor.optimize_dtypes(df)
```

#### Custom Dataset Card

```python
# Add custom metadata
card_generator.add_metadata({
    "source": "Internal Database",
    "collection_date": "2023-01-01",
    "maintainers": ["John Doe"]
})
```

#### Hugging Face Integration

```python
# Load dataset from Hugging Face
dataset = hf_manager.load_dataset("my_dataset", split="train")

# Update dataset card
hf_manager.update_dataset_card(
    dataset_name="my_dataset",
    card_path="dataset-card.json"
)
```

## Configuration

### Environment Variables

- `HUGGINGFACE_TOKEN`: Your Hugging Face API token

### Dependencies

- Python >= 3.8
- pandas >= 1.5.0
- numpy >= 1.21.0
- huggingface_hub >= 0.16.0
- datasets >= 2.12.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face for their excellent datasets library
- The pandas team for their powerful data manipulation tools
- The open-source community for their valuable contributions 