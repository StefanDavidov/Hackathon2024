import { Box, Button, Container, FormControl, InputLabel, MenuItem, Select, Typography, useMediaQuery } from '@mui/material'
import { useState } from 'react'
import InvestImage from "./images/Investing.svg"
function App() {
  const [company, setCompany] = useState('')
  const pictureShown = useMediaQuery('(min-width:1300px)');
  return (
    <Box
      sx={{ overflow: "auto", minWidth: "100vw", display: "flex", flexDirection: "column", justifyItems: "center", alignItems: "center", minHeight: "100vh" }}>
      <Container sx={{ display: "flex", justifyContent: pictureShown ? "normal" : "center", alignItems: pictureShown ? "normal" : "center" }} disableGutters={true} maxWidth={false}>
        <Box sx={{ height: "fit-content", marginLeft: (pictureShown) ? "5%" : "0%", marginTop: "5%", maxWidth: 575, }}>
          <Typography variant="h2" align="center" sx={{ fontWeight: "bold", marginTop: "2rem" }}>Insert Name here</Typography>
          <Typography variant="h4" align="center" sx={{ marginTop: "1rem" }}> A revolutionary new system for analyzing stocks</Typography>
          <Typography variant="h6" align="center" sx={{ marginTop: "1rem" }}> Pick a company</Typography>
          <Container sx={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }} disableGutters={true} maxWidth={false}>
            <FormControl sx={{ minWidth: "10em", marginTop: '2em' }}>
              <InputLabel >Company</InputLabel>
              <Select
                value={company}
                label="Company"
                onChange={(e) => setCompany(e.target.value)}
              >
                <MenuItem value={"INTC"}>Intel</MenuItem>
                <MenuItem value={"MSFT"}>Microsoft</MenuItem>
                <MenuItem value={"GOOGL"}>Alphabet</MenuItem>
                <MenuItem value={"AIZ"}>Assurant</MenuItem>
                <MenuItem value={"DE"}>John Deere</MenuItem>
              </Select>
            </FormControl>
            <Button variant='contained' sx={{ marginTop: '3em' }}>Check Prediction</Button>
          </Container>
        </Box>
        {
          (pictureShown) ? <Container sx={{ width: "calc(100vw - 800px)", justifyContent: "center", }} disableGutters={true} maxWidth={false}>
            <img src={InvestImage} style={{ zIndex: 5000, width: "100%", height: "auto", maxHeight: "calc(100vh - 6vh)", marginTop: "5vh" }} />
          </Container> : null
        }
      </Container >

    </Box >
  )
}

export default App
