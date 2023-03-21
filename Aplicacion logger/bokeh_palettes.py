# palettes.py

from bokeh.palettes import brewer, d3, Colorblind, all_palettes
from copy import copy

discrete_brewer = (brewer['Set2'][8] +
                   brewer['Set1'][9] +
                   brewer['Set3'][12] +
                   brewer['Dark2'][8])

discrete_d3 = (d3['Category20'][20][::2] +
               d3['Category20'][20][1::2])

discrete_dark = (d3['Category10'][10] +
                 brewer['Dark2'][8] +
                 Colorblind[8])


rainbow = [
    '#0034f8',
    '#0037f6',
    '#003af3',
    '#003df0',
    '#003fed',
    '#0041ea',
    '#0044e7',
    '#0046e4',
    '#0048e1',
    '#004ade',
    '#004cdb',
    '#004fd8',
    '#0051d5',
    '#0053d2',
    '#0054d0',
    '#0056cd',
    '#0058ca',
    '#005ac7',
    '#005cc4',
    '#005ec1',
    '#0060be',
    '#0061bb',
    '#0063b8',
    '#0065b6',
    '#0066b3',
    '#0068b0',
    '#006aad',
    '#006baa',
    '#006da7',
    '#006ea5',
    '#006fa2',
    '#00719f',
    '#00729d',
    '#00739a',
    '#007598',
    '#007695',
    '#077793',
    '#0d7890',
    '#13798e',
    '#187a8b',
    '#1c7b89',
    '#1f7c87',
    '#237d84',
    '#267e82',
    '#287f7f',
    '#2b807d',
    '#2d817b',
    '#2f8278',
    '#318376',
    '#328473',
    '#348571',
    '#35866f',
    '#36876c',
    '#37886a',
    '#388967',
    '#398a65',
    '#3a8b62',
    '#3b8c60',
    '#3c8e5d',
    '#3c8f5b',
    '#3d9058',
    '#3d9155',
    '#3e9253',
    '#3e9350',
    '#3e944d',
    '#3e954a',
    '#3e9647',
    '#3f9745',
    '#3f9842',
    '#3e993e',
    '#3e9a3b',
    '#3e9b38',
    '#3e9c35',
    '#3e9d32',
    '#3e9e2e',
    '#3e9f2b',
    '#3fa027',
    '#3fa124',
    '#40a221',
    '#41a31d',
    '#42a41a',
    '#44a517',
    '#45a615',
    '#47a713',
    '#4aa711',
    '#4ca80f',
    '#4fa90e',
    '#51a90d',
    '#54aa0d',
    '#57ab0d',
    '#5aab0d',
    '#5dac0d',
    '#5fad0d',
    '#62ad0e',
    '#65ae0e',
    '#67ae0e',
    '#6aaf0f',
    '#6db00f',
    '#6fb00f',
    '#72b110',
    '#74b110',
    '#77b211',
    '#79b211',
    '#7cb311',
    '#7eb412',
    '#80b412',
    '#83b512',
    '#85b513',
    '#88b613',
    '#8ab613',
    '#8cb714',
    '#8fb814',
    '#91b815',
    '#93b915',
    '#95b915',
    '#98ba16',
    '#9aba16',
    '#9cbb16',
    '#9fbb17',
    '#a1bc17',
    '#a3bc18',
    '#a5bd18',
    '#a7be18',
    '#aabe19',
    '#acbf19',
    '#aebf19',
    '#b0c01a',
    '#b2c01a',
    '#b5c11b',
    '#b7c11b',
    '#b9c21b',
    '#bbc21c',
    '#bdc31c',
    '#c0c31c',
    '#c2c41d',
    '#c4c41d',
    '#c6c51d',
    '#c8c51e',
    '#cac61e',
    '#cdc61f',
    '#cfc71f',
    '#d1c71f',
    '#d3c820',
    '#d5c820',
    '#d7c920',
    '#d9c921',
    '#dcca21',
    '#deca22',
    '#e0ca22',
    '#e2cb22',
    '#e4cb23',
    '#e6cc23',
    '#e8cc23',
    '#eacc24',
    '#eccd24',
    '#eecd24',
    '#f0cd24',
    '#f2cd24',
    '#f3cd24',
    '#f5cc24',
    '#f6cc24',
    '#f8cb24',
    '#f9ca24',
    '#f9c923',
    '#fac823',
    '#fbc722',
    '#fbc622',
    '#fcc521',
    '#fcc421',
    '#fcc220',
    '#fdc120',
    '#fdc01f',
    '#fdbe1f',
    '#fdbd1e',
    '#febb1d',
    '#feba1d',
    '#feb91c',
    '#feb71b',
    '#feb61b',
    '#feb51a',
    '#ffb31a',
    '#ffb219',
    '#ffb018',
    '#ffaf18',
    '#ffae17',
    '#ffac16',
    '#ffab16',
    '#ffa915',
    '#ffa815',
    '#ffa714',
    '#ffa513',
    '#ffa413',
    '#ffa212',
    '#ffa111',
    '#ff9f10',
    '#ff9e10',
    '#ff9c0f',
    '#ff9b0e',
    '#ff9a0e',
    '#ff980d',
    '#ff970c',
    '#ff950b',
    '#ff940b',
    '#ff920a',
    '#ff9109',
    '#ff8f08',
    '#ff8e08',
    '#ff8c07',
    '#ff8b06',
    '#ff8905',
    '#ff8805',
    '#ff8604',
    '#ff8404',
    '#ff8303',
    '#ff8102',
    '#ff8002',
    '#ff7e01',
    '#ff7c01',
    '#ff7b00',
    '#ff7900',
    '#ff7800',
    '#ff7600',
    '#ff7400',
    '#ff7200',
    '#ff7100',
    '#ff6f00',
    '#ff6d00',
    '#ff6c00',
    '#ff6a00',
    '#ff6800',
    '#ff6600',
    '#ff6400',
    '#ff6200',
    '#ff6100',
    '#ff5f00',
    '#ff5d00',
    '#ff5b00',
    '#ff5900',
    '#ff5700',
    '#ff5500',
    '#ff5300',
    '#ff5000',
    '#ff4e00',
    '#ff4c00',
    '#ff4a00',
    '#ff4700',
    '#ff4500',
    '#ff4200',
    '#ff4000',
    '#ff3d00',
    '#ff3a00',
    '#ff3700',
    '#ff3400',
    '#ff3100',
    '#ff2d00',
    '#ff2a00']

color_palettes = copy(all_palettes)
color_palettes['discrete_brewer'] = discrete_brewer
color_palettes['discrete_d3'] = discrete_d3
color_palettes['discrete_dark'] = discrete_dark
color_palettes['rainbow'] = rainbow
