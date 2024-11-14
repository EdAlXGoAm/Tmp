import React, { useEffect, useState } from "react";
import styles from '../../styles/columnRelationship.module.css';
import { mapFillViewElements } from "../../constants/MappingFilledReview/mapFillViewElements";
import { Row, Subtitle, Titles } from "../../utils/formatUtils";
import { MiddleColObjs } from "./middleColObjs";
import { Box, Tab, Tabs } from "@mui/material";

interface FileInterface {
  file?: String | null;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index, ...other }) => {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tab-panel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
      style={{ display: value === index ? 'block' : 'none' }}
    >
      <Box sx={{ p: 3 }}>
        {children}
      </Box>
    </div>
  );
};

const a11yProps = (index: number) => {
  return {
    id: `tab-${index}`,
    'aria-controls': `tabpanel-${index}`,
  };
}

const MapFillView: React.FC<FileInterface> = ({ file }) => {

  const {
    error,
    fileData,
    jsonTestCases,
    handleFileData,
  } = mapFillViewElements();

  const [value, setValue] = useState(0);

  useEffect(() => {
    if (file) {
      handleFileData(file);
    }
  }, [file]);

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <div className={styles.mapFillViewContainer}>
      <Subtitle>Mapping Filled Review</Subtitle>
      {fileData && (
        <div>
          <Subtitle mt={0}>File Data</Subtitle>
          {error && <p>{error}</p>}
          {jsonTestCases && typeof jsonTestCases === 'object' && (
            <>
              <Tabs
                value={value}
                onChange={handleChange}
                variant="scrollable"
                scrollButtons="auto"
                aria-label="TestCase Tabs"
                sx={{ borderBottom: 1, borderColor: 'divider' }}
              >
                {jsonTestCases.map((_testCase: any, i: number) => (
                  <Tab label={`TestCase ${i + 1}`} key={i} {...a11yProps(i)} />
                ))}
              </Tabs>
              {jsonTestCases.map((testCase: any, i: number) => (
                <TabPanel value={value} index={i} key={i}>
                  <div className="card-body" style={{
                    border: '1px solid grey',
                    borderRadius: '10px',
                    boxShadow: '0px 0px 20px 5px rgba(0, 0, 0, 0.1)',
                    padding: '20px'
                  }}>
                    <Titles mt={0}>{`TestCase ${i + 1}`}</Titles>
                    <Row mb={0} mt={0}>
                      {Object.entries(testCase).slice(-2).map(([key, value]: [string, any], j: number) => (
                        <MiddleColObjs key={j} mainKey={key} value={value} />
                      ))}
                    </Row>
                  </div>
                </TabPanel>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default MapFillView;
