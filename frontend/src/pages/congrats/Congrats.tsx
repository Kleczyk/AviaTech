
import React from "react";
import { useHistory } from "react-router-dom";
import { IonContent, IonPage, IonButton, IonHeader, IonToolbar, IonTitle, IonIcon } from '@ionic/react';
import { checkmarkDoneCircleOutline } from 'ionicons/icons';

import './Congrats.scss';

const Congrats: React.FC = () => {
  const history = useHistory();

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Successful verification</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <div className="congrats-page-wrap">
          <IonIcon icon={checkmarkDoneCircleOutline} color="white"></IonIcon>
          <div className="description">
            <p className="title">Happy onboarding!</p>
            <p>
              Now you can pass the gates with your <strong>FaceTicket</strong> and skip the queues.
            </p>
          </div>
          <IonButton
            size="large"
            onClick={() => history.push("/home")}
          >
            Buy new ticket
          </IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default Congrats;
