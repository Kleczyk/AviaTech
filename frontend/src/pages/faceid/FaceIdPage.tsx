
import React, { useState, useEffect } from "react";
import { IonContent, IonPage, IonButton, IonHeader, IonToolbar, IonTitle, useIonLoading } from '@ionic/react';
import { useHistory } from "react-router-dom";

import Camera from "../../components/camera/Camera";

import './FaceIdPage.scss';

const FaceIdPage: React.FC = () => {
  const history = useHistory();
  const [isScanSuccess, setIsScanSuccess] = useState(false);
  const [photo, setPhoto] = useState<string | null>(null);
  const [presentLoading, dismissLoading] = useIonLoading();

  const base64ToBlob = (base64: string, contentType: string) => {
    const byteCharacters = atob(base64.split(',')[1]);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: contentType });
  };

  const verifyPhoto = async (e: React.MouseEvent) => {
    e.preventDefault();

    if (!photo) {
      console.error('No photo taken');
      return;
    }

    const formData = new FormData();
    formData.append('passenger_name', "Joe");
    formData.append('flight_id', "44");
    console.log(photo);
    formData.append('file', base64ToBlob(photo, 'image/png'));

    try {
      const response = await fetch('http://192.168.118.1:8000/register_ticket', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('Form submitted successfully');
        console.log(response);
      } else {
        console.error('Form submission failed');
      }
    } catch (error) {
      console.error('Error submitting form: ', error);
    }
    setIsScanSuccess(true);
    dismissLoading();
  };

  useEffect( () => {
    if (!photo) {
      setIsScanSuccess(false);
    }
  }, [photo]);

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Create FaceID</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <div className="faceid-page-wrap">
          <div className="face-wrap">
            <p>
              Make a photo, so we can recognize you at the airport
            </p>
            <Camera
              photo={photo}
              setPhoto={setPhoto}
            />
          </div>
          <IonButton
            size="large"
            disabled={!photo}
            onClick={event => {
              if (isScanSuccess) {
                history.push("/congrats");
              } else {
                presentLoading({
                  message: 'Loading...',
                  // duration: 3000,
                });
                verifyPhoto(event);
              }
            }}
          >
            {isScanSuccess? "Finish" : "Send photo"}
          </IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default FaceIdPage;
