const fetch = require('isomorphic-fetch');
const fs = require('fs');

const URL = 'https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt=12-Jun-2023&todt=12-Jun-2023';

fetch(URL)
  .then(response => response.text())
  .then(data => {
    const dataFiltered = data.split('\r\n').filter(i => i);
  
    const keys = [
      'Scheme Code',
      'Scheme Name',
      'ISIN Div Payout/ISIN Growth',
      'ISIN Div Reinvestment',
      'Net Asset Value',
      'Repurchase Price',
      'Sale Price',
      'Date',
    ];
  
    let x = '';
    let y = '';
  
    const listOfScheme = [];
  
    for (const i of dataFiltered.slice(1)) {
      if (i.includes('Open Ended Schemes')) {
        x = i;
      } else if (!i.includes(';')) {
        y = i;
      } else {
        const scheme = { 'Fund Name': y, 'Category': x };
        const values = i.split(';');
  
        for (let j = 0; j < values.length; j++) {
          scheme[keys[j]] = values[j];
        }
  
        listOfScheme.push(scheme);
      }
    }
  
    const filePath = 'schemes.json';
    fs.writeFile(filePath, JSON.stringify(listOfScheme), (err) => {
      if (err) {
        console.error('Error writing file:', err);
      } else {
        console.log('File written successfully!');
      }
    });
  })
  .catch(err => {
    console.error('Error fetching data:', err);
  });
