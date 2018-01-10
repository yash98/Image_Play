public class SeamCarver {
    private Picture pic;
    private Picture temp;
    private int width;
    private int height;
    public SeamCarver(Picture picture){
        if(picture == null)  throw new IllegalArgumentException();
        this.pic = picture;
        temp = pic;
        width = pic.width();
        height = pic.height();
    }
    public Picture picture(){
        return temp;
    }
    public int width(){
        return width;
    }
    public int height(){
        return height;
    }
    private int red(int rgb){
        return (rgb >> 16) & 0xFF;
    }
    private int blue(int rgb){
        return rgb & 0xFF;
    }
    private int green(int rgb){
        return (rgb >> 8) & 0xFF;
    }
    public double energy(int x, int y){
        if(x<0 || y<0 || x>=width() || y>=height()) throw new IllegalArgumentException();
        if(x==0 || y==0 || x==width()-1 || y==height()-1) return 1000;
        int left = pic.getRGB(x-1, y);
        int right = pic.getRGB(x+1, y);
        int up = pic.getRGB(x, y-1);
        int down = pic.getRGB(x, y+1);
        double delx = Math.pow(red(left)-red(right), 2) + Math.pow(green(left)-green(right),2) + Math.pow(blue(left)-blue(right),2);
        double dely = Math.pow(red(up)-red(down), 2) + Math.pow(green(up)-green(down),2) + Math.pow(blue(up)-blue(down),2);
        return Math.sqrt(delx + dely);
    }
    public int[] findVerticalSeam(){
        double[][] picEnergy = new double[height()][width()];
        double[][] pixelDistance = new double[height()][width()];
        int[][] previous = new int[height()][width()];
        for(int i=0; i<width(); i++){
            for (int j=0; j<height(); j++){
                picEnergy[j][i] = energy(i, j);
                pixelDistance[j][i] = Double.POSITIVE_INFINITY;
            }
        }
        for(int i=0; i<width(); i++){
            pixelDistance[0][i] = 1000;
            previous[0][i] = -1;
        }
        for(int j = 0; j<height()-1; j++){
            for(int i=0; i<width(); i++ ){
                if(pixelDistance[j+1][i]>pixelDistance[j][i]+picEnergy[j+1][i]){
                    pixelDistance[j+1][i] = pixelDistance[j][i]+picEnergy[j+1][i];
                    previous[j+1][i] = i;
                }
                if(i!=width()-1) {
                    if (pixelDistance[j + 1][i + 1] > pixelDistance[j][i] + picEnergy[j + 1][i + 1]){
                        pixelDistance[j + 1][i + 1] = pixelDistance[j][i] + picEnergy[j + 1][i + 1];
                        previous[j+1][i+1] = i;
                    }
                }
                if(i!=0){
                    if(pixelDistance[j+1][i-1]>pixelDistance[j][i]+picEnergy[j+1][i-1]){
                        pixelDistance[j+1][i-1] = pixelDistance[j][i]+picEnergy[j+1][i-1];
                        previous[j+1][i-1] = i;
                    }
                }
            }
        }
        int min = 0;
        double dist = Double.POSITIVE_INFINITY;
        for(int i=0; i<width(); i++){
            if(pixelDistance[height()-1][i]<dist){
                min = i;
                dist = pixelDistance[height()-1][i];
            }
        }
        int[] out = new int[height()];
        for(int i=height()-1; i>=0; i--){
            out[i] = min;
            min = previous[i][min];
        }
        return out;
    }
    public int[] findHorizontalSeam(){
        double[][] picEnergy = new double[height()][width()];
        double[][] pixelDistance = new double[height()][width()];
        int[][] previous = new int[height()][width()];
        for(int i=0; i<width(); i++){
            for (int j=0; j<height(); j++){
                picEnergy[j][i] = energy(i, j);
                pixelDistance[j][i] = Double.POSITIVE_INFINITY;
            }
        }
        for(int i=0; i<height(); i++){
            pixelDistance[i][0] = 1000;
            previous[i][0] = -1;
        }
        for(int j = 0; j<width()-1; j++){
            for(int i=0; i<height(); i++ ){
                if(pixelDistance[i][j+1]>pixelDistance[i][j]+picEnergy[i][j+1]){
                    pixelDistance[i][j+1] = pixelDistance[i][j]+picEnergy[i][j+1];
                    previous[i][j+1] = i;
                }
                if(i!=height()-1) {
                    if (pixelDistance[i + 1][j + 1] > pixelDistance[i][j] + picEnergy[i + 1][j + 1]){
                        pixelDistance[i + 1][j + 1] = pixelDistance[i][j] + picEnergy[i + 1][j + 1];
                        previous[i+1][j+1] = i;
                    }
                }
                if(i!=0){
                    if(pixelDistance[i-1][j+1]>pixelDistance[i][j]+picEnergy[i-1][j+1]){
                        pixelDistance[i-1][j+1] = pixelDistance[i][j]+picEnergy[i-1][j+1];
                        previous[i-1][j+1] = i;
                    }
                }
            }
        }
        int min = 0;
        double dist = Double.POSITIVE_INFINITY;
        for(int i=0; i<height(); i++){
            if(pixelDistance[i][width()-1]<dist){
                min = i;
                dist = pixelDistance[i][width()-1];
            }
        }
        int[] out = new int[width()];
        for(int i=width()-1; i>=0; i--){
            out[i] = min;
            min = previous[min][i];
        }
        return out;
    }
    public void removeHorizontalSeam(int[] seam){
        if (seam == null) throw new IllegalArgumentException();
        if(height()<=1 || seam.length!=width() ) throw new IllegalArgumentException();
        if(seam[0]<0 || seam[0]>=height) throw new IllegalArgumentException();
        for(int i=0; i<width()-1; i++){
            if( seam[i+1]<0 || seam[i+1]>=height  || Math.abs(seam[i]-seam[i+1])>1) throw new IllegalArgumentException();
        }
        for(int i=0; i<width(); i++){
            int current = seam[i];
            for(int j=current; j<height()-1; j++){
                pic.set(i,j,pic.get(i,j+1));
            }
        }
        temp = new Picture(width,height-1);
        for(int i=0; i<width; i++){
            for (int j=0; j<height()-1; j++){
                temp.set(i,j,pic.get(i,j));
            }
        }
        pic = temp;
        height--;

    }
    public void removeVerticalSeam(int[] seam){
        if (seam==null) throw new IllegalArgumentException();
        if(width()<=1 || seam.length!=height()) throw new IllegalArgumentException();
        if(seam[0]<0 || seam[0]>=width) throw new IllegalArgumentException();
        for(int i=0; i<height()-1; i++){
            if( seam[i+1]<0 || seam[i+1]>=width  || Math.abs(seam[i]-seam[i+1])>1) throw new IllegalArgumentException();
        }
        for(int i=0; i<height(); i++){
            int current = seam[i];
            for(int j=current; j<width()-1; j++){
                pic.set(j,i,pic.get(j+1,i));
            }
        }
        temp = new Picture(width-1,height);
        for(int i=0; i<height; i++){
            for (int j=0; j<width()-1; j++){
                temp.set(j,i,pic.get(j,i));
            }
        }
        width--;
    }
    public static void main(String args[]){
        Picture inputImg = new Picture(args[0]);
        int removeColumns = Integer.parseInt(args[1]);
        int removeRows = Integer.parseInt(args[2]);

        //StdOut.printf("image is %d columns by %d rows\n", inputImg.width(), inputImg.height());
        SeamCarver sc = new SeamCarver(inputImg);

        //Stopwatch sw = new Stopwatch();

        for (int i = 0; i < removeRows; i++) {
            int[] horizontalSeam = sc.findHorizontalSeam();
            sc.removeHorizontalSeam(horizontalSeam);
        }

        for (int i = 0; i < removeColumns; i++) {
            int[] verticalSeam = sc.findVerticalSeam();
            sc.removeVerticalSeam(verticalSeam);
        }
        Picture outputImg = sc.picture();

        //StdOut.printf("new image size is %d columns by %d rows\n", sc.width(), sc.height());

        //StdOut.println("Resizing time: " + sw.elapsedTime() + " seconds.");
        //inputImg.show();
        //outputImg.show();
        outputImg.save(args[4] + ".jpg");
    }

}
