import CategoryOutlinedIcon from '@mui/icons-material/CategoryOutlined';
import ImageSearchOutlinedIcon from '@mui/icons-material/ImageSearchOutlined';
import PhotoLibraryOutlinedIcon from '@mui/icons-material/PhotoLibraryOutlined';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import StyleOutlinedIcon from '@mui/icons-material/StyleOutlined';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { navTo, SetScreenProps } from '../interfaces/setScreenProps';

const drawerWidth = 232;

export function Nav(props: {
  handleNav: (props: SetScreenProps) => void;
  onSettings: () => void;
}) {
  const { handleNav, onSettings } = props;
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          borderRight: '1px solid #e2e9e7',
          backgroundColor: '#fbfcfc',
        },
      }}
    >
      <Toolbar className="nav-brand">
        <Box>
          <Typography variant="overline" color="primary" fontWeight={700}>
            Collection
          </Typography>
          <Typography variant="h6" fontWeight={700} lineHeight={1.15}>
            Minion Decider
          </Typography>
        </Box>
      </Toolbar>
      <Divider />
      <List
        component="nav"
        aria-label="Main navigation"
        sx={{ px: 1.25, py: 1.5 }}
      >
        <ListItemButton
          onClick={() => handleNav(navTo.minionList({ query: {} }))}
        >
          <ListItemIcon>
            <PhotoLibraryOutlinedIcon />
          </ListItemIcon>
          <ListItemText primary="Minions" />
        </ListItemButton>
        <ListItemButton onClick={() => handleNav(navTo.tagsList({}))}>
          <ListItemIcon>
            <StyleOutlinedIcon />
          </ListItemIcon>
          <ListItemText primary="Tags" />
        </ListItemButton>
        <ListItemButton onClick={() => handleNav(navTo.scenesList({}))}>
          <ListItemIcon>
            <ImageSearchOutlinedIcon />
          </ListItemIcon>
          <ListItemText primary="Scenes" />
        </ListItemButton>
        <ListItemButton
          onClick={() => handleNav(navTo.cardImplementationsList({}))}
        >
          <ListItemIcon>
            <CategoryOutlinedIcon />
          </ListItemIcon>
          <ListItemText primary="Card implementations" />
        </ListItemButton>
      </List>
      <Box sx={{ flexGrow: 1 }} />
      <Divider />
      <List sx={{ px: 1.25, py: 1.5 }}>
        <ListItemButton onClick={onSettings} aria-label="Settings">
          <ListItemIcon>
            <SettingsOutlinedIcon />
          </ListItemIcon>
          <ListItemText primary="Settings" />
        </ListItemButton>
      </List>
    </Drawer>
  );
}
