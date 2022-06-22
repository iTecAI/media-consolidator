import "./App.scss";
import { createTheme, Theme, ThemeProvider } from "@mui/material";


export const theme: Theme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: '#5d2985',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#2d2d2d',
      paper: '#353535',
    },
  },
});

function App() {
    return <ThemeProvider theme={theme}>
        <div className="root">

        </div>
    </ThemeProvider>
}

export default App;
