import React, { useState } from "react";
import { Tabs, Tab, Box } from "@mui/material";
import TestCasesMapping from "./TestCasesMapping";
import TestCasesViewer from "./TestCasesViewer";
import TestCasesAlignAndMerge from "./TestCasesAlignAndMerge";
import MergeExcel from "./components/MergeExcel/MergeExcel";


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
      id={`tabpanel-${index}`}
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
};

export default function App() {
  const [value, setValue] = useState(0);

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <div className="container-fluid">
      <Tabs
        value={value}
        onChange={handleChange}
        variant="scrollable"
        scrollButtons="auto"
        aria-label="Navegación de Test Cases"
        sx={{ borderBottom: 1, borderColor: 'divider' }}
      >
        <Tab label="TestCase Mapping" {...a11yProps(0)} />
        <Tab label="TestCase Viewer" {...a11yProps(1)} />
        <Tab label="TestCase Align and Merge" {...a11yProps(2)} />
        <Tab label="Merge Excel" {...a11yProps(3)} />
      </Tabs>

      <TabPanel value={value} index={0}>
        <TestCasesMapping />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <TestCasesViewer />
      </TabPanel>
      <TabPanel value={value} index={2}>
        <TestCasesAlignAndMerge />
      </TabPanel>
      <TabPanel value={value} index={3}>
        <MergeExcel />
      </TabPanel>
    </div>
  );
}