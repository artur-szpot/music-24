import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#176b63', dark: '#10534d', light: '#d9eeea' },
    secondary: { main: '#b24e3d' },
    background: { default: '#f3f6f5', paper: '#ffffff' },
    text: { primary: '#202a29', secondary: '#5c6967' },
  },
  shape: { borderRadius: 6 },
  typography: {
    fontFamily: 'Roboto, sans-serif',
    h1: { fontSize: '1.75rem', fontWeight: 600 },
    h2: { fontSize: '1.25rem', fontWeight: 600 },
    button: { textTransform: 'none', fontWeight: 600 },
  },
  components: {
    MuiButton: { defaultProps: { disableElevation: true } },
    MuiAccordion: {
      styleOverrides: {
        root: { borderBottom: '1px solid #e2e9e7', boxShadow: 'none' },
      },
    },
  },
});

export default theme;
