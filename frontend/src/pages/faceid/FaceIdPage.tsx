
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

  const verifyPhoto = () => {
    console.log("requescik");
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
            onClick={() => {
              if (isScanSuccess) {
                history.push("/congrats");
              } else {
                presentLoading({
                  message: 'Loading...',
                  duration: 3000,
                });
                verifyPhoto();
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
