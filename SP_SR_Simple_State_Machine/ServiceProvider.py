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

class acceptProposal(AState):
    message_in =  ["",]       
    message_out =  ["Proposal",]
    
    def initialize(self):
        # Gaurd variables for enabling the transitions
        self.SendProposal_Enabled = True
            
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
        if (self.wait_untill_timeout(10)):
            message = self.receive(acceptProposal.message_in[0])
            self.save_in_message(message)
        
    def transitions(self) -> object:
        self.send(self.create_outbound_message(acceptProposal.message_out[0]))
        if (self.SendProposal_Enabled):
            return "SendProposal"
        
class refuseProposal(AState):
    message_in =  ["",]       
    
    def initialize(self):
        # Gaurd variables for enabling the transitions
        self.WaitforcallForProposal_Enabled = True
            
    
    def actions(self) -> None:
        if (self.wait_untill_timeout(10)):
            message = self.receive(refuseProposal.message_in[0])
            self.save_in_message(message)
        
    def transitions(self) -> object:
        if (self.WaitforcallForProposal_Enabled):
            return "WaitforcallForProposal"
        
class WaitforcallForProposal(AState):
    message_in =  ["callForProposal",]       
    
    def initialize(self):
        # Gaurd variables for enabling the transitions
        self.acceptProposal_Enabled = True
        self.refuseProposal_Enabled = True
            
    
    def actions(self) -> None:
        if (self.wait_untill_timeout(10)):
            message = self.receive(WaitforcallForProposal.message_in[0])
            self.save_in_message(message)
        
    def transitions(self) -> object:
        if (self.acceptProposal_Enabled):
            return "acceptProposal"
        if (self.refuseProposal_Enabled):
            return "refuseProposal"
        



class ServiceProvider(Actor):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''      
        Actor.__init__(self,"ServiceProvider",
                       "www.admin-shell.io/interaction/bidding",
                       "Service Provision","WaitforcallForProposal")
                        

    def start(self):
        self.run("WaitforcallForProposal")


if __name__ == '__main__':
    
    lm2 = ServiceProvider()
    lm2.Start('msgHandler')
