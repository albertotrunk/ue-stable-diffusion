from pubsub import pub

class RarestPieces(object):
    def __init__(self, piece_manager):

        self.piece_manager = piece_manager
        self.rarestPieces = []

        for pieceNumber in range(self.piece_manager.number_of_pieces):
            PeersByPiece = {"id_piece":pieceNumber, "numberOfPeers":0, "peers":[]}
            self.rarestPieces.append(PeersByPiece)

        #pub.subscribe(self.peers_bitfield, 'RarestPiece.update_peers_bitfield')


    def peers_bitfield(self,bitfield=None,peer=None,index=None):

        if len(self.rarestPieces) == 0:
            raise("no more piece")

        # Piece complete
        try:
            if not index == None:
                self.rarestPieces.__delitem__(index)
        except:
            pass

        # Peer's bitfield updated
        else:
            for i in range(len(self.rarestPieces)):
                if bitfield[i] == 1 and peer not in self.rarestPieces[i]["peers"]:
                    self.rarestPieces[i]["peers"].append(peer)
                    self.rarestPieces[i]["numberOfPeers"] = len(self.rarestPieces[i]["peers"])

    def getSortedPieces(self):
        return sorted(self.rarestPieces, key=lambda x:x['numberOfPeers'])
