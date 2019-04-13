import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitChangeProjectedFitAmount(wx.Command):

    def __init__(self, fitID, projectedFitID, amount):
        wx.Command.__init__(self, True, 'Change Projected Fit Amount')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.amount = amount
        self.savedAmount = None

    def Do(self):
        pyfalog.debug('Doing change of projected fit {} amount to {} for fit {}'.format(self.projectedFitID, self.amount, self.fitID))
        projectedFit = Fit.getInstance().getFit(self.projectedFitID)
        # Projected fit could have been deleted if we are redoing
        if projectedFit is None:
            pyfalog.debug('Projected fit is not available')
            return False
        projectionInfo = projectedFit.getProjectionInfo(self.fitID)
        if projectionInfo is None:
            pyfalog.warning('Fit projection info is not available')
            return False
        self.savedAmount = projectionInfo.amount
        # Limit to [1, 20]
        projectionInfo.amount = min(20, max(1, self.amount))
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of projected fit {} amount to {} for fit {}'.format(self.projectedFitID, self.amount, self.fitID))
        cmd = FitChangeProjectedFitAmount(self.fitID, self.projectedFitID, self.savedAmount)
        return cmd.Do()
