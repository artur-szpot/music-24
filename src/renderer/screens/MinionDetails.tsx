import React, { useEffect, useState } from 'react';
import { LoaderScreen } from '../components/Loader';
import { Minion, MINION_SIZES, MinionOwnProps } from '../components/Minion';
import { SCREEN_TYPES } from '../../enums/screens';
import { MinionDetailsOwnProps } from './MinionDetailsProps';
import { ScreenProps } from '../interfaces/screen';

export interface MinionDetailsProps
  extends MinionDetailsOwnProps,
    ScreenProps {}

export const MinionDetails: React.FC<MinionDetailsProps> = (
  props: MinionDetailsProps,
) => {
  const { id, screenType } = props;
  const [minion, setMinion] = useState<MinionOwnProps | undefined>(undefined);
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    setIsDataLoading(true);
    window.electron.database
      .minions({ ids: [id] }, 0)
      .then((result) => {
        if (!active) return undefined;
        if (result.ok) {
          setMinion(result.data[0]);
          setError(result.data.length ? '' : 'Image not found.');
        } else {
          setError(result.error.message);
        }
        setIsDataLoading(false);
        return undefined;
      })
      .catch(() => {
        if (active) {
          setError('Could not load image.');
          setIsDataLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [id]);

  if (isDataLoading) {
    return <LoaderScreen />;
  }
  if (error || !minion)
    return (
      <div className={screenType} role="alert">
        {error || 'Image not found.'}
      </div>
    );

  const size = ((_screenType: SCREEN_TYPES) => {
    switch (_screenType) {
      case SCREEN_TYPES.SCREEN:
      case SCREEN_TYPES.POPUP:
        return MINION_SIZES.SOLO;
      case SCREEN_TYPES.SIDE_PANEL:
      case SCREEN_TYPES.TOOLTIP:
        return MINION_SIZES.FULL;
      default:
        throw new Error(`Screen type not covered: ${_screenType}`);
    }
  })(screenType);

  switch (size) {
    case MINION_SIZES.SOLO:
      return (
        <div className={screenType}>
          <div className="minion-screen-contents">
            <Minion {...minion} size={size} />
          </div>
        </div>
      );
    default:
      return (
        <div className={screenType}>
          <Minion {...minion} size={size} />
        </div>
      );
  }
};
