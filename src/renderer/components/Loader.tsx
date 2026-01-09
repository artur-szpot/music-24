import CircularProgress from '@mui/material/CircularProgress';
import React from 'react';

export const LoaderScreen: React.FC<{}> = () => (
  <div className="screen">
    <p className="loading">Loading...</p>
    <CircularProgress color="inherit" />
  </div>
);

export const Loader: React.FC<{}> = () => (
  <div className="box">
    <p className="loading">Loading...</p>
    <CircularProgress color="inherit" />
  </div>
);
