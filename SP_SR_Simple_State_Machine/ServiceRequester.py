"""
Copyright (c) 2023 Otto-von-Guericke-Universitaet Magdeburg, Lehrstuhl Integrierte Automation
Author:  
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
"""

try:
    from utils.sip import Actor,AState
except ImportError:
    from src.main.utils.sip import Actor,AState

class WaitForSPProposal(AState):
    message_in =  ["proposal",]       
    
    def initialize(self):
        # Gaurd variables for enabling the transitions
        self.sendConfirmation_Enabled = True
            
    
    def actions(self) -> None:
        if (self.wait_untill_timeout(10)):
            message = self.receive(WaitForSPProposal.message_in[0])
            self.save_in_message(message)
        
    def transitions(self) -> object:
        if (self.sendConfirmation_Enabled):
            return "sendConfirmation"
        
class SendCFP(AState):
    message_out =  ["callForProposal",]
    
    def initialize(self):
        # Gaurd variables for enabling the transitions
        self.WaitForSPProposal_Enabled = True
            
    def create_outbound_message(self,msg_type) -> list:
        receiverId =""
        receiverRole = ""
        conV1 = ""
        oMessage_Out = self.create_i40_message(msg_type,conV1,receiverId,receiverRole)
        #submodel = self.GetSubmodelById('submodelId')
        #oMessage_Out["interactionElements"].append(submodel)
        self.save_out_message(oMessage_Out)
        return oMessage_Out
    
    def actions(self) -> None:
        pass
        
    def transitions(self) -> object:
        self.send(self.create_outbound_message(SendCFP.message_out[0]))
        if (self.WaitForSPProposal_Enabled):
            return "WaitForSPProposal"
        
class WaitforNewOrder(AState):
    message_in =  ["Order",]       
    
    def initialize(self):
        # Gaurd variables for enabling the transitions
        self.SendCFP_Enabled = True
            
    
    def actions(self) -> None:
        if (self.wait_untill_timeout(10)):
            message = self.receive(WaitforNewOrder.message_in[0])
            self.save_in_message(message)
        
    def transitions(self) -> object:
        if (self.SendCFP_Enabled):
            return "SendCFP"
        



class ServiceRequester(Actor):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''      
        Actor.__init__(self,"ServiceRequester",
                       "www.admin-shell.io/interaction/bidding",
                       "Service Requisition","WaitforNewOrder")
                        

    def start(self):
        self.run("WaitforNewOrder")


if __name__ == '__main__':
    
    lm2 = ServiceRequester()
    lm2.Start('msgHandler')
