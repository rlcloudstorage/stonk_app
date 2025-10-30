import pytest

from pkg.srv_scrape.client import HeatmapScraper


class TestHeatmapScraper:
    """"""
    ctx = {
        'debug': True,
        'item_pool': ['1d', '1w'],
        'command': 'heatmap',
        'url': 'https://stockanalysis.com/markets/heatmap/',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    webscraper = HeatmapScraper(ctx=ctx)


    def test_modify_heatmap_query_time_period(self, mocker):
        """return correct url?"""
        webscraper = HeatmapScraper(ctx=self.ctx)
        mock_expected = "https://stockanalysis.com/markets/heatmap/?time=1D"
        mocker.patch.object(webscraper, "_modify_heatmap_query_time_period", return_value=mock_expected)
        assert self.webscraper._modify_heatmap_query_time_period(heatmap="1d") == mock_expected


    @pytest.mark.skip("42")
    def test_return_png_img_bytes(self):
        pass


    @pytest.mark.skip("42")
    def test_save_png_image(self):
        pass
