
import React from "react";
import { IonContent, IonPage, IonButton, IonHeader, IonToolbar, IonTitle, IonItem, IonSelect, IonSelectOption, IonText, IonDatetime } from '@ionic/react';
import { useHistory } from "react-router-dom";

import './PaymentPage.scss';

const PaymentPage: React.FC = () => {
  const history = useHistory();

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Ticket Payment</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <div className="payment-wrap">
          <IonText>
            Payment...
          </IonText>
          <IonButton
            size="large"
            onClick={() => {
              history.replace("/faceid");
            }}
          >
            Finish payment
          </IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default PaymentPage;
