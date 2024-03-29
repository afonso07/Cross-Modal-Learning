import torch.nn as nn

from models import audio_encoders, text_encoders, pann_pretrain


class CRNNWordModel(nn.Module):

    def __init__(self, *args, **kwargs):
        super(CRNNWordModel, self).__init__()

        self.args = args
        self.kwargs = kwargs

        self.audio_encoder = audio_encoders.CRNNEncoder(**kwargs["audio_encoder"])

        self.text_encoder = text_encoders.WordEncoder(**kwargs["text_encoder"])

    def forward(self, audio_feats, queries, query_lens):
        """
        :param audio_feats: tensor, (batch_size, time_steps, Mel_bands).
        :param queries: tensor, (batch_size, query_max_len).
        :param query_lens: list, [N_{1}, ..., N_{batch_size}].
        :return: (batch_size, embed_dim), (batch_size, embed_dim).
        """

        audio_embeds = self.audio_encoder(audio_feats)

        query_embeds = self.text_encoder(queries, query_lens)

        # audio_embeds: [N, E]    query_embeds: [N, E]
        return audio_embeds, query_embeds


class PANNWordModel(nn.Module):
    
    def __init__(self, *args, **kwargs):
        super(PANNWordModel, self).__init__()

        self.args = args
        self.kwargs = kwargs

        self.audio_encoder = pann_pretrain.Transfer_Cnn14(**kwargs["audio_encoder"])

        self.text_encoder = text_encoders.WordEncoder(**kwargs["text_encoder"])

    def forward(self, audio_feats, queries, query_lens):
        """
        :param audio_feats: tensor, (batch_size, time_steps, Mel_bands).
        :param queries: tensor, (batch_size, query_max_len).
        :param query_lens: list, [N_{1}, ..., N_{batch_size}].
        :return: (batch_size, embed_dim), (batch_size, embed_dim).
        """

        audio_embeds = self.audio_encoder(audio_feats)

        query_embeds = self.text_encoder(queries, query_lens)

        # audio_embeds: [N, E]    query_embeds: [N, E]
        return audio_embeds, query_embeds


