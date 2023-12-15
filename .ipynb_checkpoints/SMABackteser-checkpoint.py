{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "132d0bd8-e442-486b-8502-2e7d097043a3",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "\n",
    "class SMABacktester():\n",
    "    def __init__(self,symbol,SMA_S,SMA_L,start,end):\n",
    "        self.symbol=symbol\n",
    "        self.SMA_S=SMA_S\n",
    "        self.SMA_L=SMA_L\n",
    "        self.start=start\n",
    "        self.end=end\n",
    "        self.results=None\n",
    "        self.get_data()\n",
    "        \n",
    "    def get_data(self):\n",
    "        df = yf.download(self.symbol,start=self.start,end=self.end)\n",
    "        data= df.Close.to_frame()\n",
    "        data[\"Returns\"]=np.log(data.Close.div(data.Close.shift(1)))\n",
    "        data[\"SMA_S\"]=data.Close.rolling(int(self.SMA_S)).mean()\n",
    "        data[\"SMA_L\"]=data.Close.rolling(int(self.SMA_L)).mean()\n",
    "        data.dropna(inplace=True)\n",
    "        self.data2=data\n",
    "        \n",
    "        return data\n",
    "    \n",
    "    def test_results(self):\n",
    "        data=self.data2.copy().dropna()\n",
    "        data[\"Position\"]=np.where(data[\"SMA_S\"]>data[\"SMA_L\"],1,-1)\n",
    "        data[\"Strategy\"]=data[\"Returns\"]*data.Position.shift(1)\n",
    "        data.dropna(inplace=True)\n",
    "        data[\"Returnsbh\"]=data[\"Returns\"].cumsum().apply(np.exp)\n",
    "        data[\"ReturnsStrategy\"]=data[\"Strategy\"].cumsum().apply(np.exp)\n",
    "        perf=data[\"ReturnsStrategy\"].iloc[-1]\n",
    "        outperf=perf-data[\"Returnsbh\"].iloc[-1]\n",
    "        self.results=data\n",
    "        \n",
    "        ret=np.exp(data[\"Strategy\"].sum())\n",
    "        std=data[\"Strategy\"].std()*np.sqrt(252)\n",
    "        #return ret,std\n",
    "            \n",
    "        return round(perf,6), round(outperf,6)\n",
    "    \n",
    "    def plot_results(self):\n",
    "        if self.results is None:\n",
    "            print(\"Run the test please:)\")\n",
    "        else:\n",
    "            title=\"{} SMA_S={} | SMA_L={}\".format(self.symbol,self.SMA_S,self.SMA_L)\n",
    "            self.results[[\"Returnsbh\",\"ReturnsStrategy\"]].plot(title=title, figsize=(12,8))\n",
    "        \n",
    "        "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
