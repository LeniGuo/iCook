# Recipe1M Dataset Google Drive link  
### https://drive.google.com/drive/folders/1A53LIJTx9ENsk2Y9SJS7xtCZPFReinbk?usp=drive_link
 including two pickle files of preprocessed data and indexes: `recipe_index.pkl`, `preprocessed_recipe_data.pkl`,
 two json files of initial datasets: `layer1.json`, `layer2.json` and links of other recipe databases

## Layers

### layer1.json

```js
{
  id: String,  // unique 10-digit hex string
  title: String,
  instructions: [ { text: String } ],
  ingredients: [ { text: String } ],
  partition: ('train'|'test'|'val'),
  url: String
}
```

### layer2.json

```js
{
  id: String,   // refers to an id in layer 1
  images: [ {
    id: String, // unique 10-digit hex + .jpg
    url: String
  } ]
}
```

## Images

The images in each of the partitions, train/val/test, are arranged in a four-level hierarchy corresponding to the first four digits of the image id.

For example: `val/e/f/3/d/ef3dc0de11.jpg`

The images are in RGB JPEG format and can be loaded using standard libraries.
