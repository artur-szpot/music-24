import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import App from '../renderer/App';

describe('App', () => {
  beforeEach(() => {
    window.electron = {
      config: {
        get: jest.fn(),
        choose: jest.fn(),
        apply: jest.fn(),
      },
      ipcRenderer: {
        sendMessage: jest.fn(),
        on: jest.fn(() => jest.fn()),
        once: jest.fn(),
      },
    };
  });

  it('should render', () => {
    expect(render(<App />)).toBeTruthy();
  });
});
