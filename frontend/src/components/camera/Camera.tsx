import React, { useRef, useState, useEffect } from 'react';
import { IonButton } from '@ionic/react';

import './Camera.scss';

interface Props {
  photo: string | null;
  setPhoto: (photo: string | null) => void;
}

const CameraComponent: React.FC<Props> = ({photo, setPhoto}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isTakingPhoto, setIsTakingPhoto] = useState<boolean>(true);

  useEffect(() => {
    const startCamera = async () => {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ video: true });
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.play();
          }
        } catch (error) {
          console.error('Error accessing camera: ', error);
        }
      }
    };

    if (isTakingPhoto) {
      startCamera();
    }

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, [isTakingPhoto]);

  const takePhoto = () => {
    if (canvasRef.current && videoRef.current) {
      const context = canvasRef.current.getContext('2d');
      if (context) {
        canvasRef.current.width = videoRef.current.videoWidth;
        canvasRef.current.height = videoRef.current.videoHeight;
        context.drawImage(videoRef.current, 0, 0);
        const imageUrl = canvasRef.current.toDataURL('image/png');
        setPhoto(imageUrl);
        setIsTakingPhoto(false);
      }
    }
  };

  const retakePhoto = () => {
    setPhoto(null);
    setIsTakingPhoto(true);
  };

  return (
    <div>
      {isTakingPhoto ? (
        <div className="camera-wrap">
          <video ref={videoRef} style={{ width: '100%', height: 'auto' }} />
          <IonButton onClick={takePhoto}>Take Photo</IonButton>
        </div>
      ) : (
        <div className="camera-wrap">
          <img src={photo || ''} alt="Captured" />
          <IonButton onClick={retakePhoto}>Retake Photo</IonButton>
        </div>
      )}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
};

export default CameraComponent;
