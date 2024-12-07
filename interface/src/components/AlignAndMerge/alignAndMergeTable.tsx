import React, { useEffect, useState } from 'react';
import { Table, TableRow, TableCell, TableHead, TableBody, Button, Tooltip } from '@mui/material';
import styles from '../../styles/alignAndMergeTable.module.css';
import { MiniTableButton } from '../../utils/buttonUtils';
import { alignAndMergeTableElements } from '../../constants/AlignAndMerge/alignAndMergeTableElements';
interface AlignAndMergeTableProps {
  files: string[];
  jsonObjsArray: any[];
}

export default function AlignAndMergeTable({ files, jsonObjsArray }: AlignAndMergeTableProps) {

  const {
    jsonKeys,
    jsonKeysActions, setJsonKeysActions,
    mergeContent, setMergeContent,
    onSaveMergedFile,
    fetchJsonKeys
  } = alignAndMergeTableElements({ jsonObjsArray });

  useEffect(() => {
    fetchJsonKeys(jsonObjsArray);
  }, [jsonObjsArray]);

  const [expandedCells, setExpandedCells] = useState<{ [key: string]: boolean }>({});

  const handleDoubleClick = (row: number, col: number) => {
    const key = `${row}-${col}`;
    setExpandedCells(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleJsonKeysActions = (indexFile: number, index_key: number, key: string, subKey?: string) => {
    setJsonKeysActions(prev => {
      const newArray = prev.map(innerArray => [...innerArray]);
      newArray[indexFile][index_key] = !newArray[indexFile][index_key];

      setMergeContent(prev => {
        const newMergeContentArray = prev.map(innerArray => [...innerArray]);
        console.log('Starting Set Merge Content');
        console.log(jsonObjsArray);
        for (let indexTestCase = 0; indexTestCase < jsonObjsArray[0].length; indexTestCase++) {
          let mergedContent = '';
          for (let i = 0; i < newArray.length; i++) {
            if (newArray[i][index_key]) {
              if (subKey) {
                if (typeof(jsonObjsArray[i][indexTestCase][key][subKey]) === 'string') {
                  mergedContent += (mergedContent === '' ? '' : '\n') + jsonObjsArray[i][indexTestCase][key][subKey];
                }
                else {
                  if (Array.isArray(jsonObjsArray[i][indexTestCase][key][subKey]) && jsonObjsArray[i][indexTestCase][key][subKey].length > 0) {
                    
                    const currentArray = mergedContent ? JSON.parse(mergedContent) : [];
                    const newArrayToAdd = jsonObjsArray[i][indexTestCase][key][subKey];
                    const concatenatedArray = currentArray.concat(newArrayToAdd);
                    mergedContent = concatenatedArray;
                  }
                  else {
                    mergedContent += '';
                  }
                }
              }
              else {
                console.log('i', i, 'key', key);
                console.log('newArray', newArray);
                console.log('indexTestCase', indexTestCase);
                console.log('jsonObjsArray[i]', jsonObjsArray[i]);
                console.log('jsonObjsArray[i][indexTestCase]', jsonObjsArray[i][indexTestCase]);
                if (typeof(jsonObjsArray[i][indexTestCase][key]) === 'string') {
                  mergedContent += (mergedContent === '' ? '' : '\n') + jsonObjsArray[i][indexTestCase][key];
                }
                else {
                  if (Array.isArray(jsonObjsArray[i][indexTestCase][key]) && jsonObjsArray[i][indexTestCase][key].length > 0) {
                    const currentArray = mergedContent ? JSON.parse(mergedContent) : [];
                    const newArrayToAdd = jsonObjsArray[i][indexTestCase][key];
                    const concatenatedArray = currentArray.concat(newArrayToAdd);
                    mergedContent = concatenatedArray;
                  }
                  else {
                    mergedContent += '';
                  }
                }
              }
            }
          }
          newMergeContentArray[indexTestCase][index_key] = mergedContent;
        }
        console.log('Finishing Set Merge Content');
        return newMergeContentArray;
      });

      return newArray;
    });
  }

  return (
    <>
      <Button onClick={() => onSaveMergedFile()}>Save Merged File</Button>
      <Table size="small" className={styles.table}>
        <TableHead>
          <TableRow>
            <TableCell>Test Case ID</TableCell>
            <TableCell>Keys</TableCell>
            {jsonKeys.length > 0 && files.map((file, i) => (
              <React.Fragment key={`file-${i}`}>
                <TableCell>Actions</TableCell>
                <TableCell>{file}</TableCell>
              </React.Fragment>
            ))}
            <TableCell>Merged</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {jsonObjsArray.length > 0 && jsonObjsArray[0].map((_testcases: any, i: number) => (
            jsonKeys.length > 0 && jsonKeys.map((key: string, j: number) => (
              <TableRow key={`row-${i}-${j}`}>
                <TableCell>{i}</TableCell>
                <TableCell><pre>{key}</pre></TableCell>
                {jsonObjsArray.map((testcases_obj: any, k: number) => (
                  <React.Fragment key={`cell-${i}-${j}-${k}`}>
                    {key.includes('.') ?
                      <>
                        <TableCell>
                          <MiniTableButton
                            onClick={() => handleJsonKeysActions(k, j, key.split('.')[0], key.split('.')[1])}
                            boolean_var={jsonKeysActions.length > k && jsonKeysActions[k][j]}
                            text1='On'
                            text2='Off'
                          />
                        </TableCell>
                        <TableCell
                          className={styles.tableCell}
                          onDoubleClick={() => handleDoubleClick(i, j)}
                          style={{
                            cursor: 'pointer',
                          }}
                        >
                          <Tooltip title={<pre style={{
                            color: 'white'
                          }}>{testcases_obj[i][key.split('.')[0]][key.split('.')[1]]}</pre>}
                          style={{
                            maxHeight: expandedCells[`${i}-${j}`] ? undefined : '20px',
                            userSelect: expandedCells[`${i}-${j}`] ? 'auto' : 'none'
                          }}  >
                            <div>
                              {
                                typeof testcases_obj[i][key.split('.')[0]][key.split('.')[1]] === 'string' ?
                                testcases_obj[i][key.split('.')[0]][key.split('.')[1]] !== '' ?
                                <div className={expandedCells[`${i}-${j}`] ? styles.expanded : undefined} >
                                {testcases_obj[i][key.split('.')[0]][key.split('.')[1]]}
                                </div>
                                :
                                '' :
                                Array.isArray(testcases_obj[i][key.split('.')[0]][key.split('.')[1]]) &&
                                testcases_obj[i][key.split('.')[0]][key.split('.')[1]].length > 0 ?
                                JSON.stringify(testcases_obj[i][key.split('.')[0]][key.split('.')[1]]) :
                                ''
                              }
                            </div>
                          </Tooltip>
                        </TableCell> 
                      </> :
                      <>
                        <TableCell>
                          <MiniTableButton
                            onClick={() => handleJsonKeysActions(k, j, key)}
                            boolean_var={jsonKeysActions.length > k && jsonKeysActions[k][j]}
                            text1='On'
                            text2='Off'
                          />
                        </TableCell>
                        <TableCell
                          className={styles.tableCell}
                          onDoubleClick={() => handleDoubleClick(i, j)}
                          style={{
                            cursor: 'pointer',
                          }}
                        >
                          <Tooltip title={<pre style={{
                            color: 'white'
                          }}>{testcases_obj[i][key]}</pre>}
                          style={{
                            maxHeight: expandedCells[`${i}-${j}`] ? undefined : '20px',
                            userSelect: expandedCells[`${i}-${j}`] ? 'auto' : 'none'
                          }}  >
                            <div>
                              {
                                typeof testcases_obj[i][key] === 'string' ?
                                testcases_obj[i][key] !== '' ?
                                <div className={expandedCells[`${i}-${j}`] ? styles.expanded : undefined}>
                                  {testcases_obj[i][key]}
                                </div>
                                :
                                '' :
                                Array.isArray(testcases_obj[i][key]) &&
                                testcases_obj[i][key].length > 0 ?
                                JSON.stringify(testcases_obj[i][key]) :
                                ''
                              }
                            </div>
                          </Tooltip>
                        </TableCell>
                      </>
                    }
                  </React.Fragment>
                ))}
                <TableCell
                  className={styles.tableCell}
                  onDoubleClick={() => handleDoubleClick(i, j)}
                  style={{
                    cursor: 'pointer',
                  }}
                >
                  <Tooltip title={<pre style={{
                    color: 'white'
                  }}>{mergeContent[i][j]}</pre>}
                  style={{
                    maxHeight: expandedCells[`${i}-${j}`] ? undefined : '20px',
                    userSelect: expandedCells[`${i}-${j}`] ? 'auto' : 'none'
                  }}  >
                    <div className={expandedCells[`${i}-${j}`] ? styles.expanded : undefined}>
                      {mergeContent[i][j]}
                    </div>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))
          ))}
        </TableBody>
      </Table>
    </>
  );
}
