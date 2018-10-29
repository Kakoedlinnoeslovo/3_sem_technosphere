import java.util.LinkedList;

class Utils {
    public static StringBuilder makeString(LinkedList<String> from, LinkedList<String> to){
        StringBuilder all = new StringBuilder();

        all.append("|F|");
        String sizeFrom = Integer.toString(from.size());
        String temp = sizeFrom + "\t";
        all.append(temp);

        all.append("|T|");
        String sizeTo = Integer.toString(to.size());
        temp = sizeTo + "\t";
        all.append(temp);

        for (String f : from) {
            temp = f + "\t";
            all.append(temp);
        }


        for (String t : to) {
            temp = t + "\t";
            all.append(temp);
        }
        return all;
    }
}
